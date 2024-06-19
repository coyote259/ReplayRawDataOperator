#!/usr/bin/env python
#coding:utf-8

import struct
from enum import IntEnum
import sys
import argparse
import time, pathlib, os # These parts are all only for measuring time for main loop and therefore can be deleted if deleting/commenting out time-measuring code
from crc import Calculator, Crc32  #use pip install crc to install crc module --> Python 3.7 and newer

# Image Data type enum
class DataType(IntEnum):
    FVC = 0
    SVC = 1
    SideView = 2
    #Further image data types could be added here 

# Pre or Post embedded data position
class EmbeddedDataPos(IntEnum):
    PreEmbeddedData = 0
    PostEmbeddedData = 1

#Requirement on the dataSpurce.txt: 
# 1. Every single line represents a whole embedded data line + every byte array element is separated by a space
# 2. More than 1 line may occur
#Due to small file size we prefer to use list instead of generator pattern: speed > memory
def read_data_generator(filename:str):
    with open(filename,'rt') as fin:
        line = fin.readline().strip() # the first line string without white spaces on both ends
        line_list = [[int(element,base=10) for element in line.split(sep=' ')]]
        while line:
            line = fin.readline().strip() # read next line
            #Somehow the final line is empty string
            if line != '':
                line_list.append([int(element,base=10) for element in line.split(sep=' ')])
                #print(len(line_list)) #only for debug
        #print(line_list)    #only for debug
        return line_list     # return a 2D list, in which every list-element/1D-list represents one embedded line data 

def validate_inputdata(int_arr):
    """This func validates wthether all the array elements are uint8 or not and returns a uint8 byte array python list"""
    pass


def byte_to_pixel(bytearr:list):
    """This func converts uint8 byte array python list to uint16 list, specific for RAW12 format in MIPI spec. This func should be combined with func pixel_to_byte(pixelarr)"""
    pixelarr = []
    for i in range(0,len(bytearr),3):
       lo_pixel = ((bytearr[i]<<8) |((bytearr[i+2] & 0xf) << 4)) >> 4 # take the lower 4bits of the third byte, concatenate it with the first byte(the 4bits are in lower bit position while the first whole byte is in higher bit position), finally we get a uint16 int with four padding zeros in the highest bit position 
       high_pixel = ((bytearr[i+1]<<8) |((bytearr[i+2] & 0xf0))) >> 4  #take the higher 4bits of the third byte, concatenate it with the second byte(the 4bits are in lower bit position while the second whole byte is in higher bit position), finally we get a uint16 int with four padding zeros in the highest bit position 
       pixelarr.extend([lo_pixel,high_pixel])    # when adding multiple elements, list.extend() is faster than list.append()
    #print(pixelarr) #only for debug
    return pixelarr

def pixel_to_byte(pixelarr:list):
    """This func converts uint16 pixel array to uint8 byte array, specific for RAW12 format in MIPI spec. This func should be combined with func byte_to_pixel(bytearr)"""
    bytearr = []
    for i in range(0,len(pixelarr),2):
        first_byte = pixelarr[i] >> 4  # The first byte is from 5.element on. This operation is also assumed that the highest 4 bits are all zero. If not, we should use bitmasking 0xff0 to get the 8 bits
        second_byte = pixelarr[i+1] >> 4 # ditto
        third_byte = ((pixelarr[i+1] & 0xf) << 4) | (pixelarr[i] & 0xf) # take the lower 4 bits of the second byte as higher positon and the lower 4 bits of the first byte as lower position, build a unint8
        bytearr.extend([first_byte,second_byte,third_byte]) # when adding multiple elements, list.extend() is faster than list.append()
    #print(bytearr) only for debug
    return bytearr

def increment_overwrite_fc(fc_read:int, fc_input, overwrite_fc, REGISTER_MAX):
    """This func processes(either increments or overwrites) the read framecount(fc)"""
    #Overwrite fc depending on fc_read vs. REGISTER_MAX
    if overwrite_fc:
        if fc_input <= REGISTER_MAX:
            return fc_input  # overwrite the fc with fc_input as long as REGISTER_MAX not reached
        else: 
            return 1  # reset fc to 1 
    #Increment fc depending on fc_read vs. REGISTER_MAX        
    else:
        if fc_read < REGISTER_MAX:
            return (fc_read+1)   # increment the existing fc as long as REGISTER_MAX not reached
        else:
            return 1

def process_framecount(input_firstArr:list, fc_input, overwrite_fc, REGISTER_MAX, datatype):
    """This func takes input_firstArr list as input, processes fc and CRC32 accordingly and then outputs the changed/modified input_firstArr"""
    if datatype == DataType.SVC:
        # get uint32 frame count from the 37. to 40. byte array element. Reverse the array due to little endian
        # Create a copy of the input array
        #arr_copy = input_firstArr[:]  
        arr_copy = input_firstArr.copy()
        arr = arr_copy[36:40]
        reversed_arr = arr[::-1]
        #convert 4 element u8 byte array to one U32 int
        fc_read = (reversed_arr[0] << 24) | (reversed_arr[1] << 16) | (reversed_arr[2] << 8) | reversed_arr[3]
        #Get the processed new fc
        fc_cal = increment_overwrite_fc(fc_read, fc_input, overwrite_fc, REGISTER_MAX)
        #convert the new uint32 fc to a 4-element byte array
        first_byte = fc_cal >> 24
        second_byte = (fc_cal >> 16) & 0xff
        third_byte = (fc_cal >> 8) & 0xff
        fourth_byte = fc_cal & 0xff
        arr_copy[36:40] = [fourth_byte,third_byte,second_byte,first_byte]   #reversed due to little-endian
        #print(arr_copy)  #only for debug, the fc of the input_firstArr is processed, CRC-32 recalc follows
        #CRC32 calc begins---------------------------
        crc_input = arr_copy[8:596]
        crc_calculator = Calculator(Crc32.CRC32)
        new_crc32 = crc_calculator.calculate_checksum(crc_input)
        first_crcbyte = new_crc32 >> 24
        second_crcbyte = (new_crc32>> 16) & 0xff
        third_crcbyte = (new_crc32 >> 8) & 0xff
        fourth_crcbyte = new_crc32 & 0xff
        arr_copy[596:600] = [fourth_crcbyte,third_crcbyte,second_crcbyte,first_crcbyte] #reversed due to little-endian
        # print(arr_copy) #only for debug      
        return arr_copy
        #CRC32 calc ends-------------------------------
 
    elif datatype == DataType.FVC:
        #At first converts byte array to pixel array, then processes fc, then calculates CRC and finally outputs the modified input
        pixel_arr = byte_to_pixel(input_firstArr)

        arr = pixel_arr[40:44]
        reversed_arr = arr[::-1]
        #take the 8 lower bits of every uint16 array element and then convert 4-element u8 byte array to one U32 int
        fc_read = ((reversed_arr[0] & 0xff)<< 24)  | ((reversed_arr[1] & 0xff)<< 16) | ((reversed_arr[2] & 0xff) << 8) | (reversed_arr[3] & 0xff)
        fc_cal = increment_overwrite_fc(fc_read, fc_input, overwrite_fc, REGISTER_MAX)
        #convert the new uint32 fc to a 4-element byte array
        first_byte = fc_cal >> 24
        second_byte = (fc_cal >> 16) & 0xff
        third_byte = (fc_cal >> 8) & 0xff
        fourth_byte = fc_cal & 0xff

        #write uint8 to uint16, all the high 8bits are padding 0...
        #pixel_arr[40:44] = [fourth_byte,third_byte,second_byte,first_byte]
        #Advanced: only overwrite the lower 8 bits of the four pixelarr element
        pixel_arr[40:44] = [(pixel_arr[40] & 0xff00) | fourth_byte,(pixel_arr[41] & 0xff00 )| third_byte, (pixel_arr[42] & 0xff00 )| second_byte, (pixel_arr[43] & 0xff00 )| first_byte]

        #CRC32 calc begins---------------------------
        crc_input = pixel_arr[8:900]
        crc_calculator = CrcCalculator(Crc32.CRC32)
        new_crc32 = crc_calculator.calculate_checksum(crc_input)
        first_crcbyte = new_crc32 >> 24
        second_crcbyte = (new_crc32>> 16) & 0xff
        third_crcbyte = (new_crc32 >> 8) & 0xff
        fourth_crcbyte = new_crc32 & 0xff
        #write uint8 to uint16, all the high 8bits are padding 0
        #pixel_arr[900:904] = [fourth_crcbyte,third_crcbyte,second_crcbyte,first_crcbyte]
        #Advanced: only overwrite the lower 8 bits of the four pixelarr element
        pixel_arr[900:904] = [(pixel_arr[900] & 0xff00) | fourth_crcbyte,(pixel_arr[901] & 0xff00) | third_crcbyte,(pixel_arr[902] & 0xff00) | second_crcbyte,(pixel_arr[903] & 0xff00) | first_crcbyte]
        #print(byte_to_pixel(pixel_to_byte))   # Only for debug
        return pixel_to_byte(pixel_arr)      
        #CRC calc ends-------------------------------

    elif datatype == DataType.SideView:
        #At first converts byte array to pixel array, then processes fc, then calculates CRC and finally outputs the modified input
        pixel_arr = byte_to_pixel(input_firstArr)

        arr = pixel_arr[36:40]
        reversed_arr = arr[::-1]
        #take the 8 lower bits of every uint16 array element and then convert 4-element u8 byte array to one U32 int
        fc_read = ((reversed_arr[0] & 0xff)<< 24)  | ((reversed_arr[1] & 0xff)<< 16) | ((reversed_arr[2] & 0xff) << 8) | (reversed_arr[3] & 0xff)
        fc_cal = increment_overwrite_fc(fc_read, fc_input, overwrite_fc, REGISTER_MAX)
        #convert the new uint32 fc to a 4-element byte array
        first_byte = fc_cal >> 24
        second_byte = (fc_cal >> 16) & 0xff
        third_byte = (fc_cal >> 8) & 0xff
        fourth_byte = fc_cal & 0xff

        #write uint8 to uint16, all the high 8bits are padding 0...
        #pixel_arr[36:40] = [fourth_byte,third_byte,second_byte,first_byte]
        #Advanced: only overwrite the lower 8 bits of the four pixelarr element
        pixel_arr[36:40] = [(pixel_arr[36] & 0xff00) | fourth_byte,(pixel_arr[37] & 0xff00 )| third_byte, (pixel_arr[38] & 0xff00 )| second_byte, (pixel_arr[39] & 0xff00 )| first_byte]

        #CRC32 calc begins---------------------------
        crc_input = pixel_arr[8:596]
        crc_calculator = Calculator(Crc32.CRC32)
        new_crc32 = crc_calculator.calculate_checksum(crc_input)
        first_crcbyte = new_crc32 >> 24
        second_crcbyte = (new_crc32>> 16) & 0xff
        third_crcbyte = (new_crc32 >> 8) & 0xff
        fourth_crcbyte = new_crc32 & 0xff
        #write uint8 to uint16, all the high 8bits are padding 0
        #pixel_arr[596:600] = [fourth_crcbyte,third_crcbyte,second_crcbyte,first_crcbyte]
        #Advanced: only overwrite the lower 8 bits of the four pixelarr element
        pixel_arr[596:600] = [(pixel_arr[596] & 0xff00) | fourth_crcbyte,(pixel_arr[597] & 0xff00) | third_crcbyte,(pixel_arr[598] & 0xff00) | second_crcbyte,(pixel_arr[599] & 0xff00) | first_crcbyte]
        #print(byte_to_pixel(pixel_to_byte))   # Only for debug
        return pixel_to_byte(pixel_arr)      
        #CRC calc ends-------------------------------

    else:
        raise Exception("Wrong image data type is given, only FVC, SVC and SideView are supported!")
    

def adjust_data_for_hdmisender(input_bytearr:list,datatype):
    """This func adds three bytes in front of the output byte array list to ajdust HDMISender"""

    if datatype == DataType.FVC:
        #Datatype of RAW12 is 0x2C 
        input_bytearr.insert(0,0x2C)

    elif datatype == DataType.SVC:
        #Datatype of YUV422_8bit is 0x1E
        input_bytearr.insert(0,0x1E)
        
    elif datatype == DataType.SideView:
        #Datatype of RAW12 is 0x2C
        input_bytearr.insert(0,0x2C)       
    
    else:
        raise Exception("Wrong image data type is given, only FVC, SVC and SideView are supported!")
    
    length = len(input_bytearr) - 1
    #The first two bytes (little endian) makes up a uint16 int to indicate the byte number of the current line
    #insert higher 8bits in front of the array/list   
    input_bytearr.insert(0, (length >> 8) & 0xff )
    #insert lower 8bits in front of the array/list
    input_bytearr.insert(0,length & 0xff)

    return input_bytearr 

def write_linecount_to_stdout(linecount:int):
    """This func converts the uint16 input to little-endian and then write it the begin of every frame"""
    #Write the little-endian uint16 to the begin of every frame
    try:
        sys.stdout.buffer.write(linecount.to_bytes(2,'little',signed=False))
    except OverflowError:
        raise Exception('line count in a single frame is bigger than 65535')

def write_data_to_stdout(input_bytearr:list):
    #input_bytearr is a list
    sys.stdout.buffer.write(bytes(input_bytearr))

def main(filename:str,embeddedDataPos, fc_input, overwrite_fc, REGISTER_MAX,datatype,counter:int):
    """docstring needed"""

    # Process pre embedded data
    if embeddedDataPos == EmbeddedDataPos.PreEmbeddedData:
        #Read the data source from file
        # Regardless of how many lines there are in the source file,
        # only the first line will be processed with fc and CRC, other the following lines will be just be passed to stdout without any modification
        read_array = read_data_generator(filename) # read all pre embedded lines

        linecount_pre = len(read_array)
        write_linecount_to_stdout(linecount_pre)
        
        # pick the 1st line to process fc and CRC
        input_firstArr,input_otherArr = read_array[0], read_array[1:] 

        #instead of assigned to processed_arr(point to the same object), processed_arr[:] (two different objects)
        processed_array, processed_otherArr = [], [[]]
        processed_array[:] = processed_arr = process_framecount(input_firstArr,fc_input,overwrite_fc,REGISTER_MAX,datatype)
        output_arr = adjust_data_for_hdmisender(processed_arr,datatype)
        #Write the modified first embedded line to stdout
        write_data_to_stdout(output_arr)
        #Write all the following embedded lines unchanged to stdout
        if len(input_otherArr) > 0:
            for output_otherArr in input_otherArr:
                processed_otherArr.append(adjust_data_for_hdmisender(output_otherArr,datatype))
                sys.stdout.buffer.write(processed_otherArr[-1])
        loop_counter_pre = 1

        while True:
            #The following times process_framecount() only increments fc
            # If counter is uint, then loop times are counter time; otherwise infinite loop    
            if (loop_counter_pre < counter) or (counter < 0):
                
                write_linecount_to_stdout(linecount_pre)

                processed_array[:] = processed_arr = process_framecount(processed_array,fc_input,False,REGISTER_MAX,datatype)
                output_arr = adjust_data_for_hdmisender(processed_arr,datatype)
                write_data_to_stdout(output_arr)

                if len(processed_otherArr) > 0:
                    for output_otherArr in processed_otherArr:
                        write_data_to_stdout(output_otherArr)

                loop_counter_pre+=1
                time.sleep(0.015)
                continue
            else:
                break     

    # Process post embedded data            
    elif embeddedDataPos == EmbeddedDataPos.PostEmbeddedData:
        loop_counter_post = 1
        output_array =read_data_generator(filename)
        stdout_array = [[]]

        linecount_post = len(output_array)
        write_linecount_to_stdout(linecount_post)

        for input_array in output_array:
            stdout_array.append(adjust_data_for_hdmisender(input_array,datatype))
            write_data_to_stdout(stdout_array[-1])

        while True:
            if (loop_counter_post < counter) or (counter < 0):

                write_linecount_to_stdout(linecount_post)
                
                for output in stdout_array:
                    write_data_to_stdout(output)
                loop_counter_post +=1
                time.sleep(0.015)
                continue

            else:
                break

    else:
        raise Exception("Invalid input for embedded data position, 0 for pre, 1 for post!")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PreEmbedded data processing - framecount and CRC32')
    parser.add_argument('--filename', type=str, default=r"C:\Users\qilli\MeineProjekte\Projekt_II_ADAS_HIL_Replay\Aufgabe1\Python_Script\testErgebnis\dataSource_Post_RAW12.txt",help="Data source of embedded data")
    parser.add_argument('--embeddedDataPos',type=int, default=EmbeddedDataPos.PreEmbeddedData, help='switch to process pre pr post embedded data, 0 for pre, 1 for post.')
    parser.add_argument('--fc_input', type=int, default=10, help='User-defined frame count for the first output to stdout,default is 10')
    parser.add_argument('--overwrite_fc', type=bool, default=False, help='Toggle switch to enable user-defined frame count input or not, default is false')
    parser.add_argument('--REGISTER_MAX', type=int, default=0xFFFFFFFF, help='Simulate the register maxvalue,default is 0xFFFFFFFF. When frame count reaches this value, the next frame count will be reset to 1')
    parser.add_argument('--datatype', type=int, default=DataType.FVC, help='image data type, 0 for FVC, 1 for SVC, 2 for SideView. Up to now only these two data types are supported')
    parser.add_argument('--counter', type=int, default=-1, help='loop counter, default -1 means infinite loop and programm can only be killed/stopped by external program')

    args = parser.parse_args()
    filename = args.filename
    embeddedDataPos = args.embeddedDataPos
    fc_input = args.fc_input
    overwrite_fc = args.overwrite_fc
    REGISTER_MAX = args.REGISTER_MAX
    datatype = args.datatype
    counter = args.counter

    start_time = time.time()

    try:

        main(filename,embeddedDataPos,fc_input,overwrite_fc,REGISTER_MAX,datatype,counter)
    
    except KeyboardInterrupt:

        sys.stdout.buffer.flush()
        sys.exit(0)
    
    end_time = time.time()
    
    #0 suffix means preEmbeddedData, 1 suffix means Post
    filepath = os.path.join(pathlib.Path(__file__).parent,f'time{embeddedDataPos}.txt')
    with open(filepath,'at') as fout:
        fout.write(f'{embeddedDataPos} started (0 for Pre, 1 for Post)\n')
        fout.write(f'start time: {start_time}s\n')
        fout.write(f'end time: {end_time}s\n')
        if counter > 0:
            fout.write(f'total time for {counter} loops: {end_time-start_time}s\n')
            fout.write(f'average time: {(end_time-start_time)/counter}s\n')
        fout.write(f'--------------------------------\n')
     





<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="20008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="ctl" Type="Folder" URL="../ctl">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="subVI" Type="Folder" URL="../subVI">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="ebd" Type="Folder" URL="../ebd">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="toplevel_VI" Type="Folder" URL="../toplevel_VI">
			<Property Name="NI.DISK" Type="Bool">true</Property>
		</Item>
		<Item Name="tools" Type="Folder"/>
		<Item Name="Rawdata_Generator.vi" Type="VI" URL="../Rawdata_Generator.vi"/>
		<Item Name="Rawdata_Generator_2.vi" Type="VI" URL="../Rawdata_Generator_2.vi"/>
		<Item Name="Rawdata_Analyzer.vi" Type="VI" URL="../Rawdata_Analyzer.vi"/>
		<Item Name="Rawdata_Viewer.vi" Type="VI" URL="../Rawdata_Viewer.vi"/>
		<Item Name="Rawdata_Embdata_Analyer.vi" Type="VI" URL="../Rawdata_Embdata_Analyer.vi"/>
		<Item Name="Rawdata_Metadata_Generator.vi" Type="VI" URL="../Rawdata_Metadata_Generator.vi"/>
		<Item Name="Rawdata_Metadata_Analyzer.vi" Type="VI" URL="../Rawdata_Metadata_Analyzer.vi"/>
		<Item Name="Rawdata_Imagedata_Generator.vi" Type="VI" URL="../Rawdata_Imagedata_Generator.vi"/>
		<Item Name="Rawdata_Imagedata_Analyzer.vi" Type="VI" URL="../Rawdata_Imagedata_Analyzer.vi"/>
		<Item Name="Timestamp_Analyzer.vi" Type="VI" URL="../Timestamp_Analyzer.vi"/>
		<Item Name="Timestamp_Compare.vi" Type="VI" URL="../Timestamp_Compare.vi"/>
		<Item Name="Frame_Drop_Analyzer.vi" Type="VI" URL="../Frame_Drop_Analyzer.vi"/>
		<Item Name="265_data.vi" Type="VI" URL="../265_data.vi"/>
		<Item Name="FFMPEG_Timestamp_Generator.vi" Type="VI" URL="../FFMPEG_Timestamp_Generator.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Color (U64)" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Color (U64)"/>
				<Item Name="Image Type" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Image Type"/>
				<Item Name="IMAQ ArrayToColorImage" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ArrayToColorImage"/>
				<Item Name="IMAQ Bayer To RGB" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Bayer To RGB"/>
				<Item Name="IMAQ ColorImageToArray" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ColorImageToArray"/>
				<Item Name="IMAQ Create" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Create"/>
				<Item Name="IMAQ Image Bit Depth" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Image Bit Depth"/>
				<Item Name="IMAQ Image.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/IMAQ Image.ctl"/>
				<Item Name="IMAQ ImageToEDVR 1D CSG.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 1D CSG.vi"/>
				<Item Name="IMAQ ImageToEDVR 1D I16.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 1D I16.vi"/>
				<Item Name="IMAQ ImageToEDVR 1D SGL.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 1D SGL.vi"/>
				<Item Name="IMAQ ImageToEDVR 1D U8.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 1D U8.vi"/>
				<Item Name="IMAQ ImageToEDVR 1D U16.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 1D U16.vi"/>
				<Item Name="IMAQ ImageToEDVR 1D U32.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 1D U32.vi"/>
				<Item Name="IMAQ ImageToEDVR 1D U64.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 1D U64.vi"/>
				<Item Name="IMAQ ImageToEDVR 2D CSG.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 2D CSG.vi"/>
				<Item Name="IMAQ ImageToEDVR 2D I16.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 2D I16.vi"/>
				<Item Name="IMAQ ImageToEDVR 2D SGL.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 2D SGL.vi"/>
				<Item Name="IMAQ ImageToEDVR 2D U8.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 2D U8.vi"/>
				<Item Name="IMAQ ImageToEDVR 2D U16.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 2D U16.vi"/>
				<Item Name="IMAQ ImageToEDVR 2D U32.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 2D U32.vi"/>
				<Item Name="IMAQ ImageToEDVR 2D U64.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 2D U64.vi"/>
				<Item Name="IMAQ ImageToEDVR 3D I16.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 3D I16.vi"/>
				<Item Name="IMAQ ImageToEDVR 3D SGL.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 3D SGL.vi"/>
				<Item Name="IMAQ ImageToEDVR 3D U8.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 3D U8.vi"/>
				<Item Name="IMAQ ImageToEDVR 3D U16.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR 3D U16.vi"/>
				<Item Name="IMAQ ImageToEDVR.vi" Type="VI" URL="/&lt;vilib&gt;/vision/EDVR.llb/IMAQ ImageToEDVR.vi"/>
				<Item Name="IMAQ SetImageSize" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ SetImageSize"/>
				<Item Name="NI_Vision_Development_Module.lvlib" Type="Library" URL="/&lt;vilib&gt;/vision/NI_Vision_Development_Module.lvlib"/>
				<Item Name="RGB to Color.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/colorconv.llb/RGB to Color.vi"/>
				<Item Name="Color to RGB.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/colorconv.llb/Color to RGB.vi"/>
				<Item Name="System Exec.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/System Exec.vi"/>
				<Item Name="Random Number (Range).vi" Type="VI" URL="/&lt;vilib&gt;/numeric/Random Number (Range).vi"/>
				<Item Name="Random Number (Range) DBL.vi" Type="VI" URL="/&lt;vilib&gt;/numeric/Random Number (Range) DBL.vi"/>
				<Item Name="Random Number (Range) I64.vi" Type="VI" URL="/&lt;vilib&gt;/numeric/Random Number (Range) I64.vi"/>
				<Item Name="sub_Random U32.vi" Type="VI" URL="/&lt;vilib&gt;/numeric/sub_Random U32.vi"/>
				<Item Name="Random Number (Range) U64.vi" Type="VI" URL="/&lt;vilib&gt;/numeric/Random Number (Range) U64.vi"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="IMAQ Dispose" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Dispose"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Remove Duplicates From 1D Array.vim" Type="VI" URL="/&lt;vilib&gt;/Array/Remove Duplicates From 1D Array.vim"/>
			</Item>
			<Item Name="nivision.dll" Type="Document" URL="nivision.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="nivissvc.dll" Type="Document" URL="nivissvc.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>

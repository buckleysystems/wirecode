<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="20008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="count_integrations.vi" Type="VI" URL="../count_integrations.vi"/>
		<Item Name="generate_square_plan.vi" Type="VI" URL="../generate_square_plan.vi"/>
		<Item Name="get_python_library_path.vi" Type="VI" URL="../get_python_library_path.vi"/>
		<Item Name="label_integrals.vi" Type="VI" URL="../label_integrals.vi"/>
		<Item Name="plan_to_coordinates.vi" Type="VI" URL="../plan_to_coordinates.vi"/>
		<Item Name="plan_to_grbl.vi" Type="VI" URL="../plan_to_grbl.vi"/>
		<Item Name="test.vi" Type="VI" URL="../test.vi"/>
		<Item Name="test_generator.vi" Type="VI" URL="../test_generator.vi"/>
		<Item Name="write_results.vi" Type="VI" URL="../write_results.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>

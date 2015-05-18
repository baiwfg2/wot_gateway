整个Python网关中间件工程包含在wot_gateway文件夹内，各文件夹及文件功能简述如下：

cfg/
	dev_property.xml: 设备属性信息（向平台添加设备时用到）
	gw_property.xml: 网关属性信息（网关注册时用到）
	res_property.xml: 资源属性信息（向平台添加资源时用到）
	
	gw_json.cfg: json格式配置文件，目前包括3个域
		updated:网关是否已经更新过
		mwid:网关在平台上的ID
		hwid:网关硬件ID，目前用MAC地址指代
	local.cfg: 平台相关配置，包括平台IP,服务器端口号，各开放接口URL
	
	mac_dev_map.cfg: hwid与设备号的本地映射表
	mac_resID_resPlat_map.cfg:hwid、本地资源ID（我们自己定义的）和平台资源ID的本地映射表

lib/
	campra_thread.py: 摄像头线程模块 

	common.py: 通用模块，包括获取MAC地址、写配置文件等

	gateway.py: 网关核心类，封装了网关注册、网关更新、删除网关、添加/删除设备、添加/删除资源、上传传感器数据/图像等

	heartbeat.py: 心跳线程模块，用于定时向平台上传心跳，获取平台上的操作指令

	init.py: 初使化模块，用以读local.cfg配置文件

	main.cfg: json格式配置文件

	main.py：主模块，调用示例

	register.py: 网关注册线程

	res_data.py: 传感器数据上传线程

	restful.py: GET,POST请求python方法封装
	
log/
	日志，目前维护较少


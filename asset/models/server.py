# -*- coding:utf8 -*-
"""
Created on 2017/6/28 2:35
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models
from cmdb.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin


class LogicalServer(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    逻辑服务器, 用来抽象物理机/云主机/虚拟机等不同类型的资源, 具备业务属性.
    """
    LOGICAL_SERVER_STATUS_CHOICES = (
        ('shutdown', '关机'),
        ('running', '运行'),
        ('setup', '开机'),
        ('fault', '故障'),
        ('online', '在线'),
        ('offline', '下线')
    )

    LOGICAL_SERVER_LIVE_CYCLE_CHOICES = (
        ('approve', '审批'),
        ('purchasing', '采购'),
        ('already', '就绪'),
        ('recycle', '回收'),
        ('maintaining', '报修'),
        ('obsolete', '报废')
    )

    hostname = models.CharField(max_length=30, unique=True, help_text='逻辑服务器主机名, 通常用于标识业务归属')
    operation_system = models.ForeignKey(OperationSystem, on_delete=models.SET_NULL, help_text='操作系统')
    model = models.ForeignKey(ServerModel, on_delete=models.SET_NULL, help_text='服务器型号')
    physical_server = models.ForeignKey(PhysicalServer, on_delete=models.SET_NULL, blank=True, help_text='所属宿主机')
    department = models.PositiveIntegerField(blank=True, help_text='资产归属部门')
    status = models.CharField(choices=LOGICAL_SERVER_STATUS_CHOICES, max_length=20, help_text='服务器状态')
    live_cycle = models.CharField(choices=LOGICAL_SERVER_LIVE_CYCLE_CHOICES, max_length=20, help_text='服务器生命周期')

    def __str__(self):
        return self.hostname


class PhysicalServer(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    物理服务器
    """
    PHYSICAL_SERVER_LIVE_CYCLE_CHOICES = (
        ('purchasing', '采购'),
        ('shelve', '上架'),
        ('unshelve', '下架'),
        ('maintaining', '报修'),
        ('obsolete', '报废')
    )

    PHYSICAL_SERVER_STATUS_CHOICES = (
        ('shutdown', '关机'),
        ('running', '运行'),
        ('setup', '开机'),
        ('fault', '故障'),
        ('online', '在线'),
        ('offline', '下线')
    )

    asset_id = models.CharField(max_length=20, unique=True, help_text='服务器资产编号,服务器的唯一标识')
    sn = models.CharField(max_length=20, unique=True, help_text='主机节点SN编号,用于唯一标识服务器,不可变')
    model = models.ForeignKey(ServerModel, on_delete=models.SET_NULL, help_text='服务器型号')
    provider = models.ForeignKey(, blank=True,  help_text='服务器硬件供应商')
    idc = models.ForeignKey(, blank=True,  help_text='IDC供应商,为idc表主键ID')
    rack_id = models.CharField(blank=True,  max_length=20, help_text='机架ID')
    slot = models.CharField(blank=True,  max_length=20, help_text='机架中槽位ID')
    status = models.CharField(choices=PHYSICAL_SERVER_STATUS_CHOICES, max_length=20, help_text='服务器状态')
    live_cycle = models.CharField(choices=PHYSICAL_SERVER_LIVE_CYCLE_CHOICES, max_length=20, help_text='服务器生命周期')

    def __str__(self):
        return self.asset_id


class OperationSystem(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    操作系统
    """
    OPERATION_SYSTEM_TYPE = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
        ('bsd', 'BSD'),
        ('osx', 'MacOSX'),
        ('unix', 'Unix')
    )

    os_type = models.CharField(help_text='操作系统类型,可用值为: 0->Windows、1->Linux、2->BSD、3->MacOSX')
    name = models.CharField(max_length=10, help_text='操作系统发行版,例如: CentOS、RHEL、Windows')
    version = models.CharField(max_length=10, help_text='主版本号')
    minor_version = models.CharField(blank=True,  max_length=10, help_text='次版本号')
    kernel_version = models.CharField(blank=True, max_length=50, help_text='内核版本')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __str__(self):
        return u'-'.join((self.name, self.version, self.minor_version))


class ServerModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    服务器型号
    """

    SERVER_TYPE_CHOICES = (
        ('physical', '物理机'),
        ('kvm', 'kvm虚拟机'),
        ('xen', 'xen虚拟机'),
        ('cloud', '云主机')
    )

    brand = models.CharField(max_length=10, help_text='品牌名称,为英文或者中文拼音')
    alias = models.CharField(max_length=30, help_text='品牌别名、全称')
    series = models.CharField(max_length=20, help_text='系列,例如：S720')
    model = models.CharField(max_length=30, help_text='型号')
    server_type = models.CharField(max_length=15, choices=SERVER_TYPE_CHOICES, help_text='主机类型')
    cpu_model = models.ForeignKey(ServerCPUModel, on_delete=models.SET_NULL, blank=True, help_text='CPU型号')
    cpu_num = models.SmallIntegerField(default=1, help_text='物理CPU个数')
    memory_model = models.ForeignKey(ServerMemoryModel, on_delete=models.SET_NULL, help_text='内存型号')
    memory_num = models.PositiveSmallIntegerField(default=1, help_text='内存卡个数')
    disk_num = models.SmallIntegerField(default=1, help_text='标配磁盘个数')
    disk_model = models.ForeignKey(ServerHardDiskModel, on_delete=models.SET_NULL, help_text='磁盘型号')
    nic_model = models.ForeignKey(ServerNicModel, on_delete=models.SET_NULL, help_text='网卡型号')
    nic_num = models.PositiveSmallIntegerField(default=1, help_text='网卡个数')

    def __str__(self):
        return '-'.join((self.brand, self.series, self.model))


class ServerCPUModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    服务器CPU型号
    """
    brand = models.CharField(max_length=10, help_text='品牌名称,为英文或者中文拼音')
    alias = models.CharField(max_length=30, help_text='品牌别名、全称')
    series = models.CharField(max_length=20, help_text='系列')
    model = models.CharField(max_length=50, help_text='型号')
    core_num = models.PositiveSmallIntegerField(help_text='cpu 核心数')
    basic_frequency = models.FloatField(blank=True, help_text='CPU 主频, 单位为: GHz')
    hyper_threading = models.BooleanField(default=True, help_text='是否支持超线程')

    def __str__(self):
        return '-'.join((self.brand, self.series, self.model))


class ServerMemoryModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    服务器内存型号
    """
    brand = models.CharField(max_length=10, help_text='品牌名称,为英文或者中文拼音')
    alias = models.CharField(max_length=30, help_text='品牌别名、全称')
    series = models.CharField(max_length=20, help_text='系列')
    model = models.CharField(max_length=50, help_text='型号')
    frequency = models.FloatField(help_text='内存支持的最高频率,单位为：GHz')
    size = models.PositiveIntegerField(help_text='内存容量, 单位为: MB')

    def __str__(self):
        return '-'.join((self.brand, self.series, self.model))


class ServerMemory(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    服务器内存
    """
    sn = models.CharField(max_length=30, unique=True, help_text='内存编号,用于唯一标识内存卡,不可变')
    server = models.ForeignKey(PhysicalServer, on_delete=models.SET_NULL, help_text='所属服务器', blank=True)
    model = models.ForeignKey(ServerMemoryModel, on_delete=models.SET_NULL, help_text='内存型号')
    is_extend = models.BooleanField(default=False, help_text='内存卡是否为扩展,True为扩展,False为该服务器标配')

    def __str__(self):
        return self.sn


class ServerNicModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    服务器网卡型号
    """
    brand = models.CharField(max_length=10, help_text='品牌名称,为英文或者中文拼音')
    alias = models.CharField(max_length=30, help_text='品牌别名、全称')
    series = models.CharField(max_length=20, help_text='系列')
    virtual = models.BooleanField(help_text='是否为虚拟网卡')
    model = models.CharField(max_length=50, help_text='网卡型号')
    speed = models.CharField(max_length=10, help_text='网卡支持的最高速率,格式为：1000Mbps')

    def __str__(self):
        return '-'.join((self.brand, self.series, self.model))


class ServerNic(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    服务器网卡
    """
    sn = models.CharField(max_length=30, unique=True, help_text='网卡编号,用于唯一标识网卡,不可变')
    server = models.ForeignKey(LogicalServer, on_delete=models.SET_NULL, help_text='所属服务器', blank=True)
    model = models.ForeignKey(ServerNicModel, on_delete=models.SET_NULL, help_text='网卡型号')
    is_extend = models.BooleanField(default=False, help_text='网卡是否为扩展,True为扩展,False为该服务器标配')
    mac = models.CharField(max_length=12, unique=True, help_text='MAC地址,格式为：FFFFFFFFFFFF')
    ip = models.GenericIPAddressField(blank=True,  unique=True, help_text='网卡IP地址')
    speed = models.CharField(max_length=10, help_text='网卡实际工作速率,格式为：1000Mbps')
    duplex = models.BooleanField(default=True, help_text='网卡实际双工模式, 是否为全双工.')

    def __str__(self):
        return self.sn


class ServerHardDiskModel(models.Model):
    """
    服务器硬盘型号
    """
    HARD_DISK_TYPE_CHOICES = (
        ('HD', '常规硬盘'),
        ('SSD', '固态硬盘'),
        ('VHD', '虚拟硬盘, 例如虚拟机磁盘及云存储'),
        ('FLASH', '闪存')
    )

    brand = models.CharField(max_length=10, help_text='品牌名称,为英文或者中文拼音')
    alias = models.CharField(max_length=30, help_text='品牌别名、全称')
    series = models.CharField(max_length=20, help_text='系列')
    model = models.CharField(max_length=50, help_text='型号')
    os_type = models.CharField(max_length=10, choices=HARD_DISK_TYPE_CHOICES, help_text='硬盘类型')

    disk_size = models.IntegerField(help_text='磁盘容量,单位为：MB')
    random_read_speed = models.IntegerField(blank=True, help_text='磁盘随机读速率, 单位byte/s')
    random_write_speed = models.IntegerField(blank=True, help_text='磁盘随机写速率, 单位byte/s')
    sequential_read_speed = models.IntegerField(blank=True, help_text='磁盘顺序读速率, 单位byte/s')
    sequential_write_speed = models.IntegerField(blank=True, help_text='磁盘顺序写速率, 单位byte/s')

    def __str__(self):
        return '-'.join((self.brand, self.series, self.model))


class ServerHardDisk(models.Model):
    """
    服务器硬盘
    """
    sn = models.CharField(max_length=30, unique=True, help_text='存储编号,用于唯一标识存储,不可变')
    model = models.ForeignKey(ServerHardDiskModel, on_delete=models.SET_NULL, help_text='硬盘型号')
    is_extend = models.BooleanField(default=False, help_text='存储是否为扩展,True为扩展,Flase为该服务器型号自带')
    server = models.ForeignKey(LogicalServer, on_delete=models.SET_NULL, help_text='所属服务器', blank=True)

    def __str__(self):
        return self.sn


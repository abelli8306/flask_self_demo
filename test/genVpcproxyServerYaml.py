#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import re
import os.path
import yaml


def formartParams(excel_file_abspath, excel_sheetname):
    '''[summary]
    [description]
        format params
        formartParams("/tmp/scf_tokyo_0325.xlsx","vpc_proxy")
    Arguments:
        excel_file_abspath {[str]} -- [excel file name full path]
        excel_sheetname {[str]} -- [excel sheet name]
    '''
    isExists = os.path.exists(excel_file_abspath)
    if not isExists:
        res = excel_file_abspath + ' ,file is not exist!'
        return res

    # global common yaml
    f1 = open('./common.yaml', 'r')
    config = yaml.load(f1, Loader=yaml.FullLoader)
    # 注意：此处配置文件加载未做严格判断校验
    # print config

    # 过滤规则
    filterrule = 'vpc_proxy'

    # 加载excel数据
    # for windows
    # d1 = pd.read_excel("C:\\Users\\markuszhu\\Desktop\\scf_tokyo_0325.xlsx", sep='\t', sheet_name="vpc_proxy")
    d1 = pd.read_excel(excel_file_abspath,
                       sheet_name=excel_sheetname, sep='\t')

    # for linux
    # d1 = pd.read_excel("/tmp/scf_tokyo_0325.xlsx", sep='\t', sheet_name="vpc_proxy")
    # print d1.columns

    # # 获取filterrule指定的数据，按照第一列cloud_resource过滤
    df = d1
    df = d1.head(8)
    vpcdata = df[df['cloud_resource'] == filterrule]
    # A = vpcdata[['jnsgw_ip', 'jnsgw_port', 'rs_ip', 'rs_port','vpc_gw_ip','vpc_gw_port']]
    # print A
    group = vpcdata.groupby('rs_ip').groups
    res_dict = {}
    for g in group:
        # print g
        d_dict = {}
        d = df[df['rs_ip'] == g][['jnsgw_ip', 'jnsgw_port',
                                  'rs_ip', 'rs_port', 'vpc_gw_ip', 'vpc_gw_port']]
        # print d[['jnsgw_ip', 'jnsgw_port', 'rs_ip', 'rs_port', 'vpc_gw_ip', 'vpc_gw_port']]
        # for i in d.index:
        for i in range(0, len(d)):
            # d_dict[str(d.ix[i]['rs_port'])] = str(d.ix[i]['jnsgw_ip']) + ':' + str(d.ix[i]['jnsgw_port'])
            d_dict[str(d.iloc[i]['rs_port'])] = str(
                d.iloc[i]['jnsgw_ip']) + ':' + str(d.iloc[i]['jnsgw_port'])
            # print(i)
            # print(d.iloc[i]['jnsgw_port'])
            # print(d_dict)
            # break
            # print d_dict
            # break

        res_dict[str(g)] = d_dict
        res_dict[str(g)]['vpcid'] = str(config['vpcid'])
        res_dict[str(g)]['vpcgw'] = str(config['vpcgw'])
        res_dict[str(g)]['region_name'] = str(config['region_name'])
        res_dict[str(g)]['region'] = str(config['region'])
        res_dict[str(g)]['scflogkey'] = str(config['scflog']['secretkey'])
        res_dict[str(g)]['scflogulsdestid'] = str(
            config['scflog']['ulsdestid'])
        res_dict[str(g)]['scflogdestid'] = str(config['scflog']['destid'])
        # break

    return res_dict


def genVpcproxyCfg(dict_info):
    '''
    生成vpc_proxy的配置文件 server.yaml
    '''
    vpcgw = dict_info['vpcgw']
    vpcid = dict_info['vpcid']
    jns_gw_invokerAddr = dict_info['50051']
    jns_gw_deployerAddr = dict_info['50052']
    jns_gw_placeagentAddr = dict_info['50013']
    region_name = dict_info['region_name']
    region = dict_info['region']
    scflogkey = dict_info['scflogkey']
    scflogulsdestid = dict_info['scflogulsdestid']
    scflogdestid = dict_info['scflogdestid']

    cfgtpl = '''\
# vpc_proxy server.yaml
etcd:
    # etcdController地址信息
    addr:  ''' + vpcgw + '''
    addr1: ''' + vpcgw + '''
    addr2: ''' + vpcgw + '''
    dialTimeout: 5
    requestTimeout: 5

heartbeat:
    timeout: 10
    vpcId:  ''' + vpcid + '''
    invokerAddr: ''' + jns_gw_invokerAddr + '''  #map port 50051
    invokerKey: v2/''' + region_name + '''/heartbeat/vpc_proxy/invoker
    deployerAddr: ''' + jns_gw_deployerAddr + '''  #map port 50052
    deployerKey: v2/''' + region_name + '''/heartbeat/vpc_proxy/deployer
    placeagentAddr: ''' + jns_gw_placeagentAddr + '''  #map port 50013
    placeagentKey: v2/''' + region_name + '''/heartbeat/vpc_proxy/placeagent

worker:
    invokerPort: 50051
    deployerPort: 50052
    placeagentPort: 50013
    dialTimeout: 5
    requestTimeout: 300
    healthCheckGap: 300

eth:
    defaultIp: 0.0.0.0
    name: eth0

grpc:
    maxMsgSize: 67108864
    concurrentStreams: 100000

scflog:
    path: /usr/local/services/vpc_proxy-1.0/log/
    fileSize: 200
    fileNum: 20
    region: ''' + region + '''
    # FATAL 级别日志的告警密钥: https://qcloud.oa.com/yuntu/index.php/alarm/alarm_access
    alarmSecretKey: ''' + scflogkey + ''' #告警秘钥
    # 流水日志上报到 uls 的数据集ID
    ulsLevel: 2
    # ulsDestId: ''' + scflogulsdestid + ''' #日志集id,待修改
    # destId: ''' + scflogdestid + '''  #模调id,待修改

'''

    return cfgtpl


def saveVpcproxyCfg(data, fileprefix='tmp', relativepath='tmpetc'):
    '''[summary]

    [description] 保存vpc_proxy的配置文件 server.yaml

    Arguments:scf_tokyo_0325
        data {[yaml]} -- [yaml格式]
        fileprefix {[str]} -- [文件名前缀]
    '''

    cfg_path = os.path.abspath('.') + '/' + relativepath + '/'
    # cfg_path = os.path.dirname(os.getcwd()) + '/tmpetc/'
    cfg_name = cfg_path + fileprefix + '.server.yaml'
    # print cfg_path
    isExists = os.path.exists(cfg_path)
    if not isExists:
        os.makedirs(cfg_path)

    # Method 1
    # with open(cfg_name, "w") as f:
    #     yaml.safe_dump(data, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    # Method 2
    data = bytes(data, encoding="utf8")
    f = open(cfg_name, 'wb')
    f.write(data)
    f.close()


if __name__ == '__main__':

    # 初始化配置文件
    params_dict = {}
    # params_dict = formartParams("etc/scf_tokyo_0325.xlsx", 'vpc_proxy')
    params_dict = formartParams('C:\\Users\\xiaoboli\\Downloads\\scf_tokyo_0325.xlsx', 'vpc_proxy')
    print(params_dict)

    # 生成server.yaml
    for rs_ip in params_dict:
        rs_cfg = params_dict[rs_ip]
        rs_data = genVpcproxyCfg(rs_cfg)
        saveVpcproxyCfg(rs_data, fileprefix=rs_ip)
        # print rs_data
        # break

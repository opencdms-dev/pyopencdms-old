""" MCH API ver 0.1
Author: Etna Cervantes
License: CC-BY-SA 4.0

2020 Mexico
"""
from flask import Flask, jsonify, json, Response
from flask_restful import Api, Resource, reqparse, abort
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
import json
from os.path import abspath, dirname, join

app = Flask(__name__)
# Mysql connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='eporrasc'
app.config['MYSQL_DB']='mcheng'
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
mysql = MySQL(app)
api = Api(app)

# dataframe for stations table
stnmdata = pd.DataFrame()       

# read MCH languaje definition from mch.dbn
filemch = open('mch.dbn', 'r')
filemch.readline() # odbc connector
filemch.readline() # mysql5
filemch.readline() # interface languaje
mchlang = filemch.readline() # database languaje

# read fields and tables names definition file
deftbfl = pd.read_csv('MCHtablasycampos.def', sep = "\t", names = ['sec','type', 'id_sec', 'esp', 'eng', 'fra', '4', 'comment'], encoding='utf_8')

# new dataframe for especific languaje
ltbfl = pd.DataFrame()

# looking for especific fields and tables for the languaje
if int(mchlang) == 1:
    ltbfl = deftbfl[['id_sec','esp']]
    ltbfl.set_index('id_sec')
if int(mchlang) == 2:
    ltbfl = deftbfl[['id_sec','eng']]
    ltbfl.set_index('id_sec')
if int(mchlang) == 3:
    ltbfl = deftbfl[['id_sec','fra']]
    ltbfl.set_index('id_sec')

def deg_to_dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]


class stations(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstaciones']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        strqry='select * from ' +stntable.iloc[0,1] +' order by ' +stnfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Station','StationName','StationName2','TimeZone','Longitude','Latitude','Altitude','Longitude2','Latitude2','DMSlongitude','DMSLatitude','Statee','RegManagmt','Catchment','Subcatchment',
                                'OperatnlRegion','HydroReg','RH(2)','Municipality','CodeB','CodeG','CodeCB','CodePB','CodeE','CodeCL','CodeHG','CodePG','CodeNw','Code1','Code2','Code3','MaxOrdStrgLvl','MaxOrdStrgVol',
                                'MaxExtStrgLvl','MaxExtStrgVol','SpillwayLevel','SpillwayStorage','FreeSpillwayLevel','FreeSpillwayStorage','DeadStrgLevel','DeadStrgCapac','UsableStorageCapLev','UsableStorage','HoldingStorage',
                                'Key1fil','Key2fil','Key3fil','CritLevelSta','MinLevelSta','MaxLevelSta','CritFlow','MinDischarge','MaxDischarge','Stream','Distance','Infrastructure','Type','Usee'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(stations, "/API/stations")

qry_station_req_arg = reqparse.RequestParser()
pars = qry_station_req_arg.add_argument("stn_id",type=str,help="Station ID",required=True)

class qry_station(Resource):
    def get(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstaciones']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        parser = reqparse.RequestParser()
        parser.add_argument('stn_id')
        args = parser.parse_args()
        stn_id = args.get('stn_id')
        strqry='select * from ' +stntable.iloc[0,1] +' where ' +stnfield.iloc[0,1] +'="'+ stn_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        qrystation = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=qrystation,columns=['Station','StationName','StationName2','TimeZone','Longitude','Latitude','Altitude','Longitude2','Latitude2','DMSlongitude','DMSLatitude','Statee','RegManagmt','Catchment','Subcatchment',
                                'OperatnlRegion','HydroReg','RH','Municipality','CodeB','CodeG','CodeCB','CodePB','CodeE','CodeCL','CodeHG','CodePG','CodeNw','Code1','Code2','Code3','MaxOrdStrgLvl','MaxOrdStrgVol',
                                'MaxExtStrgLvl','MaxExtStrgVol','SpillwayLevel','SpillwayStorage','FreeSpillwayLevel','FreeSpillwayStorage','DeadStrgLevel','DeadStrgCapac','UsableStorageCapLev','UsableStorage','HoldingStorage',
                                'Key1fil','Key2fil','Key3fil','CritLevelSta','MinLevelSta','MaxLevelSta','CritFlow','MinDischarge','MaxDischarge','Stream','Distance','Infrastructure','Type','Usee'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="Station not found...")
        #abort_if_stn_not_exist("stn_id")
        return parsed

    def post(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstaciones']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('stn_id')
        parser.add_argument('stn_name')
        parser.add_argument('stn_name2')
        parser.add_argument('t_zone')
        parser.add_argument('long')
        parser.add_argument('lat')
        parser.add_argument('alt')
        parser.add_argument('state_id')
        parser.add_argument('reg_m')
        parser.add_argument('catchm')
        parser.add_argument('s_cat')
        parser.add_argument('o_reg')
        parser.add_argument('hydro_r')
        parser.add_argument('rh')
        parser.add_argument('mun_id')
        parser.add_argument('mosl')
        parser.add_argument('mosv')
        parser.add_argument('mesl')
        parser.add_argument('mesv')
        parser.add_argument('s_level')
        parser.add_argument('s_stor')
        parser.add_argument('fs_level')
        parser.add_argument('fs_stor')
        parser.add_argument('ds_level')
        parser.add_argument('ds_cap')
        parser.add_argument('us_capl')
        parser.add_argument('ustor')
        parser.add_argument('hstor')
        parser.add_argument('crl_s')
        parser.add_argument('mnl_s')
        parser.add_argument('mxl_s')
        parser.add_argument('cr_f')
        parser.add_argument('mn_dis')
        parser.add_argument('mx_dis')
        parser.add_argument('stream')
        parser.add_argument('dist')
        parser.add_argument('infr')
        parser.add_argument('type')
        parser.add_argument('use')
        args = parser.parse_args()
        # retrieve parameters
        jfile = args.get('file')
        stn_id = args.get('stn_id')
        stn_name = args.get('stn_name')
        stn_name2 = args.get('stn_name2')
        t_zone = args.get('t_zone')
        long2 = args.get('long')
        lat2 = args.get('lat')
        alt = args.get('alt')
        state_id = args.get('state_id')
        reg_m = args.get('reg_m')
        catchm = args.get('catchm')
        s_cat = args.get('s_cat')
        o_reg = args.get('o_reg')
        hydro_r = args.get('hydro_r')
        rh = args.get('rh')
        mun_id = args.get('mun_id')
        mosl = args.get('mosl')
        mosv = args.get('mosv')
        mesl = args.get('mesl')
        mesv = args.get('mesv')
        s_level = args.get('s_level')
        s_stor = args.get('s_stor')
        fs_level = args.get('fs_level')
        fs_stor = args.get('fs_stor')
        ds_level = args.get('ds_level')
        ds_cap = args.get('ds_cap')
        us_capl = args.get('us_capl')
        ustor = args.get('ustor')
        hstor = args.get('hstor')
        crl_s = args.get('crl_s')
        mnl_s = args.get('mnl_s')
        mxl_s = args.get('mxl_s')
        cr_f = args.get('cr_f')
        mn_dis = args.get('mn_dis')
        mx_dis = args.get('mx_dis')
        stream = args.get('stream')
        dist = args.get('dist')
        infr = args.get('infr')
        typee = args.get('type')
        usee = args.get('use')
        # check if input is at file
        if jfile in (None, ''):
            Latitude=deg_to_dms(float(lat2))
            Longitude=deg_to_dms(float(long2))
            slong2=str(Longitude[0])+'°'+str(Longitude[1]) +'´' +str(Longitude[2])
            slat2=str(Latitude[0])+'°'+str(Latitude[1]) +'´' +str(Latitude[2])
            strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +str(stn_id) +'","' +str(stn_name) +'","' +str(stn_name2) +'","' +str(t_zone) +'","' + str(long2)
                    + '","' +str(lat2) +'","' +str(alt) +'","' +str(long2) +'","' +str(lat2) +'","' +slong2 +'","' +slat2 +'","' +str(state_id) +'","' +str(reg_m)
                    + '","' +str(catchm) +'","' +str(s_cat) +'","' +str(o_reg) +'","' +str(hydro_r) +'","' +str(rh) +'","' +str(mun_id) +'","","","","","","","","","","","","","' + str(mosl)
                    + '","' +str(mosv) +'","' +str(mesl) +'","' +str(mesv) +'","' +str(s_level) +'","' +str(s_stor) +'","' +str(fs_level) +'","' + str(fs_stor)
                    + '","' +str(ds_level) +'","' +str(ds_cap) +'","' +str(us_capl) +'","' +str(ustor) +'","' +str(hstor) +'","","","","' +str(crl_s) +'","' + str(mnl_s)
                    + '","' +str(mxl_s) +'","' +str(cr_f) +'","' +str(mn_dis) +'","' +str(mx_dis) +'","' +str(stream) +'","' +str(dist) +'","' +str(infr) +'","' + str(typee)
                    + '","' +str(usee) +'")')   
            qry.execute(strqry)        
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows:
                    strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'","' +data.iloc[int(n),3] +'","' + data.iloc[int(n),4]
                        + '","' +data.iloc[int(n),5] +'","' +str(data.iloc[int(n),6]) +'","' +str(data.iloc[int(n),7]) +'","' +str(data.iloc[int(n),8]) +'","' +data.iloc[int(n),9] +'","' +data.iloc[int(n),10] +'","' +data.iloc[int(n),11]
                        + '","' +data.iloc[int(n),12]  + '","' +data.iloc[int(n),13] +'","' +data.iloc[int(n),14] +'","' +data.iloc[int(n),15] +'","' +data.iloc[int(n),16] +'","' +data.iloc[int(n),17] +'","' +data.iloc[int(n),18]
                        + '","' +data.iloc[int(n),19] +'","' +data.iloc[int(n),20] +'","' +data.iloc[int(n),21] +'","' +data.iloc[int(n),22] +'","' +data.iloc[int(n),23] +'","' +data.iloc[int(n),24] +'","' +data.iloc[int(n),25]
                        + '","' +data.iloc[int(n),26] + '","' +data.iloc[int(n),27] +'","' +data.iloc[int(n),28] +'","' +data.iloc[int(n),29] +'","' +data.iloc[int(n),30] +'","' +data.iloc[int(n),31]
                        + '","' +data.iloc[int(n),32] +'","' +data.iloc[int(n),33] +'","' +data.iloc[int(n),34] +'","' +data.iloc[int(n),35] +'","' +data.iloc[int(n),36] +'","' +data.iloc[int(n),37] +'","' + data.iloc[int(n),38]
                        + '","' +data.iloc[int(n),39] +'","' +data.iloc[int(n),40] +'","' +data.iloc[int(n),41] +'","' +data.iloc[int(n),42] +'","' +data.iloc[int(n),43] +'","' +data.iloc[int(n),44] +'","' +data.iloc[int(n),45]
                        + '","' +data.iloc[int(n),46] +'","' +data.iloc[int(n),47] +'","' + data.iloc[int(n),48] +'","' +data.iloc[int(n),49] +'","' +data.iloc[int(n),50] +'","' +data.iloc[int(n),51] +'","' +data.iloc[int(n),52]
                        + '","' +data.iloc[int(n),53] +'","' +data.iloc[int(n),54] +'","' +data.iloc[int(n),55] +'","' +data.iloc[int(n),56] +'","' +data.iloc[int(n),57] +'")') 
                    qry.execute(strqry) 
            else:
                strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] +'","' +data.iloc[0,3] +'","' + data.iloc[0,4]
                        + '","' +data.iloc[0,5] +'","' +str(data.iloc[0,6]) +'","' +str(data.iloc[0,7]) +'","' +str(data.iloc[0,8]) +'","' +data.iloc[0,9] +'","' +data.iloc[0,10] +'","' +data.iloc[0,11]
                        + '","' +data.iloc[0,12]  + '","' +data.iloc[0,13] +'","' +data.iloc[0,14] +'","' +data.iloc[0,15] +'","' +data.iloc[0,16] +'","' +data.iloc[0,17] +'","' +data.iloc[0,18]
                        + '","' +data.iloc[0,19] +'","' +data.iloc[0,20] +'","' +data.iloc[0,21] +'","' +data.iloc[0,22] +'","' +data.iloc[0,23] +'","' +data.iloc[0,24] +'","' +data.iloc[0,25]
                        + '","' +data.iloc[0,26] + '","' +data.iloc[0,27] +'","' +data.iloc[0,28] +'","' +data.iloc[0,29] +'","' +data.iloc[0,30] +'","' +data.iloc[0,31]
                        + '","' +data.iloc[0,32] +'","' +data.iloc[0,33] +'","' +data.iloc[0,34] +'","' +data.iloc[0,35] +'","' +data.iloc[0,36] +'","' +data.iloc[0,37] +'","' + data.iloc[0,38]
                        + '","' +data.iloc[0,39] +'","' +data.iloc[0,40] +'","' +data.iloc[0,41] +'","' +data.iloc[0,42] +'","' +data.iloc[0,43] +'","' +data.iloc[0,44] +'","' +data.iloc[0,45]
                        + '","' +data.iloc[0,46] +'","' +data.iloc[0,47] +'","' + data.iloc[0,48] +'","' +data.iloc[0,49] +'","' +data.iloc[0,50] +'","' +data.iloc[0,51] +'","' +data.iloc[0,52]
                        + '","' +data.iloc[0,53] +'","' +data.iloc[0,54] +'","' +data.iloc[0,55] +'","' +data.iloc[0,56] +'","' +data.iloc[0,57] +'")')
                qry.execute(strqry)
        return 'Station stored',201

    def delete(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstaciones']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        parser = reqparse.RequestParser()
        parser.add_argument('stn_id')
        args = parser.parse_args()
        stn_id = args.get('stn_id')
        strqry='delete from ' +stntable.iloc[0,1] +' where ' +stnfield.iloc[0,1] +'="'+ stn_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Station deleted',204

    
api.add_resource(qry_station, "/API/stations/qry_station")

class stngroups(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntGruposestac']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncGrupoEstac']
        strqry='select distinct(' +nfield.iloc[0,1] +') from ' +ntable.iloc[0,1] +' order by ' +nfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Stngroup'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(stngroups, "/API/stngroups")

class qry_stngroup(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntGruposestac']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncGrupoEstac']
        parser = reqparse.RequestParser()
        parser.add_argument('stngp_id')
        args = parser.parse_args()
        stngp_id = args.get('stngp_id')
        strqry='select * from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ stngp_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=dataqry,columns=['Stngroup','Secuen','Station'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="Stationgroup not found...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntGruposestac']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncGrupoEstac']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        f=open(jfile,'r')
        filej = f.read()  
        f.close()
        jdata = json.loads(filej)
        data = pd.DataFrame(jdata)
        tdata=len(data.index)
        rows=list(range(0,tdata))
        for n in rows:
            strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'")') 
            qry.execute(strqry)
        return 'Stationgroup stored',201
    def delete(self):
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntGruposestac']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncGrupoEstac']
        parser = reqparse.RequestParser()
        parser.add_argument('stngp_id')
        args = parser.parse_args()
        stngp_id = args.get('stngp_id')
        strqry='delete from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ stngp_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Stationgroup deleted',204


api.add_resource(qry_stngroup, "/API/stngroups/qry_stngroup")

class variables(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntVariables']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncVariable']
        strqry='select distinct(' +nfield.iloc[0,1] +') from ' +ntable.iloc[0,1] +' order by ' +nfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Variable'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(variables, "/API/variables")

class qry_variable(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntVariables']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncVariable']
        parser = reqparse.RequestParser()
        parser.add_argument('var_id')
        args = parser.parse_args()
        var_id = args.get('var_id')
        strqry='select * from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ var_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=dataqry,columns=['Variable','VariabAbbrev','VariabDescrn','TableName','Unit','TypeDDorDE','CumulType','NbrDecimal','CalcbyGrp','CalcDTaD'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="Variable not found...")
        return parsed

api.add_resource(qry_variable, "/API/variables/qry_variable")

class states(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntEstados']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncEstado']
        strqry='select * from ' +ntable.iloc[0,1] +' order by ' +nfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Statee','State2','Statename'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(states, "/API/states")

class qry_state(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntEstados']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncEstado']
        parser = reqparse.RequestParser()
        parser.add_argument('state_id')
        args = parser.parse_args()
        state_id = args.get('state_id')
        strqry='select * from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ state_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=dataqry,columns=['Statee','State2','Statename'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="State not found...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstados']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstado']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('state_id')
        parser.add_argument('state_2')
        parser.add_argument('state_name')
        args = parser.parse_args()
        # retrieve parameters
        jfile = args.get('file')
        state_id = args.get('state_id')
        state_2 = args.get('state_2')
        state_name = args.get('state_name')
        # check if input is at file
        if jfile in (None, ''):
            strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +str(state_id) +'","' +str(state_2) +'","' +str(state_name) +'")')   
            qry.execute(strqry)        
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows:
                    strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'")') 
                    qry.execute(strqry) 
            else:
                strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] +'")')
                qry.execute(strqry)
        return 'State stored',201
    def delete(self):
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntEstados']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncEstado']
        parser = reqparse.RequestParser()
        parser.add_argument('state_id')
        args = parser.parse_args()
        stngp_id = args.get('state_id')
        strqry='delete from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ state_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'State deleted',204

api.add_resource(qry_state, "/API/states/qry_state")

class municipalities(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntMunicipios']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncMunicipio']
        strqry='select * from ' +ntable.iloc[0,1] +' order by ' +nfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Municipality','Municipality2','MunicipalityName'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(municipalities, "/API/municipalities")

class qry_municipality(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntMunicipios']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncMunicipio']
        parser = reqparse.RequestParser()
        parser.add_argument('mun_id')
        args = parser.parse_args()
        mun_id = args.get('mun_id')
        strqry='select * from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ mun_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=dataqry,columns=['Municipality','Municipality2','MunicipalityName'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="Municipality not found...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntMunicipios']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncMunicipio']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('mun_id')
        parser.add_argument('mun_2')
        parser.add_argument('mun_name')
        args = parser.parse_args()
        # retrieve parameters
        jfile = args.get('file')
        mun_id = args.get('mun_id')
        mun_2 = args.get('mun_2')
        mun_name = args.get('mun_name')
        # check if input is at file
        if jfile in (None, ''):
            strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +str(mun_id) +'","' +str(mun_2) +'","' +str(mun_name) +'")')   
            qry.execute(strqry)        
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows:
                    strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'")') 
                    qry.execute(strqry) 
            else:
                strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] +'")')
                qry.execute(strqry)
        return 'Municipality stored',201
    def delete(self):
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntMunicipios']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncMunicipio']
        parser = reqparse.RequestParser()
        parser.add_argument('mun_id')
        args = parser.parse_args()
        stngp_id = args.get('mun_id')
        strqry='delete from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ mun_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Municipality deleted',204

api.add_resource(qry_municipality, "/API/municipalities/qry_municipality")

class hydroregions(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntRegionhidr']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncReghidr']
        strqry='select * from ' +ntable.iloc[0,1] +' order by ' +nfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Hydroreg','Hydroreg2','HydrRegionName'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(hydroregions, "/API/hydroregions")

class qry_hydroregion(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntRegionhidr']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncReghidr']
        parser = reqparse.RequestParser()
        parser.add_argument('hr_id')
        args = parser.parse_args()
        hr_id = args.get('hr_id')
        strqry='select * from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ hr_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=dataqry,columns=['Hydroreg','Hydroreg2','HydrRegionName'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="Hydro Region not found...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntRegionhidr']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncReghidr']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('hr_id')
        parser.add_argument('hr_2')
        parser.add_argument('hr_name')
        args = parser.parse_args()
        # retrieve parameters
        jfile = args.get('file')
        hr_id = args.get('hr_id')
        hr_2 = args.get('hr_2')
        hr_name = args.get('hr_name')
        # check if input is at file
        if jfile in (None, ''):
            strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +str(hr_id) +'","' +str(hr_2) +'","' +str(hr_name) +'")')   
            qry.execute(strqry)        
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows:
                    strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'")') 
                    qry.execute(strqry) 
            else:
                strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] +'")')
                qry.execute(strqry)
        return 'Hydrological Region stored',201
    def delete(self):
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntRegionhidr']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncReghidr']
        parser = reqparse.RequestParser()
        parser.add_argument('hr_id')
        args = parser.parse_args()
        hr_id = args.get('hr_id')
        strqry='delete from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ hr_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Hydrological Region deleted',204

api.add_resource(qry_hydroregion, "/API/hydroregions/qry_hydroregion")

class catchments(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntCuencas']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncCuenca']
        strqry='select * from ' +ntable.iloc[0,1] +' order by ' +nfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Catchment','Catchment2','CatchmentName'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(catchments, "/API/catchments")

class qry_catchment(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntCuencas']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncCuenca']
        parser = reqparse.RequestParser()
        parser.add_argument('cat_id')
        args = parser.parse_args()
        cat_id = args.get('cat_id')
        strqry='select * from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ cat_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=dataqry,columns=['Catchment','Catchment2','CatchmentName'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="Catchment not found...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntCuencas']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncCuenca']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('cat_id')
        parser.add_argument('cat_2')
        parser.add_argument('cat_name')
        args = parser.parse_args()
        # retrieve parameters
        jfile = args.get('file')
        cat_id = args.get('cat_id')
        cat_2 = args.get('cat_2')
        cat_name = args.get('cat_name')
        # check if input is at file
        if jfile in (None, ''):
            strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +str(cat_id) +'","' +str(cat_2) +'","' +str(cat_name) +'")')   
            qry.execute(strqry)        
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows:
                    strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'")') 
                    qry.execute(strqry) 
            else:
                strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] +'")')
                qry.execute(strqry)
        return 'Catchment stored',201
    def delete(self):
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntCuencas']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncCuenca']
        parser = reqparse.RequestParser()
        parser.add_argument('cat_id')
        args = parser.parse_args()
        cat_id = args.get('cat_id')
        strqry='delete from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ cat_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Catchment deleted',204

api.add_resource(qry_catchment, "/API/catchments/qry_catchment")

class subcatchments(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntSubcuencas']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncSubcuenca']
        strqry='select * from ' +ntable.iloc[0,1] +' order by ' +nfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Subcatchment','Subcatchment2','SubCatchmentName'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(subcatchments, "/API/subcatchments")

class qry_subcatchment(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntSubcuencas']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncSubcuenca']
        parser = reqparse.RequestParser()
        parser.add_argument('scat_id')
        args = parser.parse_args()
        scat_id = args.get('scat_id')
        strqry='select * from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ scat_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=dataqry,columns=['Subcatchment','Subcatchment2','SubCatchmentName'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="Subcatchment not found...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntSubcuencas']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncSubcuenca']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('scat_id')
        parser.add_argument('scat_2')
        parser.add_argument('scat_name')
        args = parser.parse_args()
        # retrieve parameters
        jfile = args.get('file')
        scat_id = args.get('scat_id')
        scat_2 = args.get('scat_2')
        scat_name = args.get('scat_name')
        # check if input is at file
        if jfile in (None, ''):
            strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +str(scat_id) +'","' +str(scat_2) +'","' +str(scat_name) +'")')   
            qry.execute(strqry)        
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows:
                    strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'")') 
                    qry.execute(strqry) 
            else:
                strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] +'")')
                qry.execute(strqry)
        return 'Subcatchment stored',201
    def delete(self):
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntSubcuencas']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncSubcuenca']
        parser = reqparse.RequestParser()
        parser.add_argument('scat_id')
        args = parser.parse_args()
        scat_id = args.get('scat_id')
        strqry='delete from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ scat_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Subcatchment deleted',204

api.add_resource(qry_subcatchment, "/API/subcatchments/qry_subcatchment")

class units(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntUnidades']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncUnidad']
        strqry='select * from ' +ntable.iloc[0,1] +' order by ' +nfield.iloc[0,1]
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        stnmdata = pd.DataFrame(data=dataqry,columns=['Unit','UnitDescription'])
        jsondata = stnmdata.to_json(orient="records")
        parsed = json.loads(jsondata)
        return parsed

api.add_resource(units, "/API/units")

class qry_unit(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntUnidades']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncUnidad']
        parser = reqparse.RequestParser()
        parser.add_argument('unit_id')
        args = parser.parse_args()
        unit_id = args.get('unit_id')
        strqry='select * from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ unit_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            stnmdata = pd.DataFrame(data=dataqry,columns=['Unit','UnitDescription'])
            jsondata = stnmdata.to_json(orient="records")
            parsed = json.loads(jsondata)
        else:
            abort(404, message="Unit not found...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        stntable = ltbfl[ltbfl['id_sec'] == 'ntUnidades']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncUnidad']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('unit_id')
        parser.add_argument('unit_desc')
        args = parser.parse_args()
        # retrieve parameters
        jfile = args.get('file')
        unit_id = args.get('unit_id')
        unit_desc = args.get('unit_desc')
        # check if input is at file
        if jfile in (None, ''):
            strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +str(unit_id) +'","' +str(unit_desc) +'")')   
            qry.execute(strqry)        
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows:
                    strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[int(n),0] +'")') 
                    qry.execute(strqry) 
            else:
                strqry = ('insert ignore into ' +stntable.iloc[0,1] +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'")')
                qry.execute(strqry)
        return 'Unit stored',201
    def delete(self):
        qry = mysql.connection.cursor()
        ntable = ltbfl[ltbfl['id_sec'] == 'ntUnidades']
        nfield = ltbfl[ltbfl['id_sec'] == 'ncUnidad']
        parser = reqparse.RequestParser()
        parser.add_argument('unit_id')
        args = parser.parse_args()
        unit_id = args.get('unit_id')
        strqry='delete from ' +ntable.iloc[0,1] +' where ' +nfield.iloc[0,1] +'="'+ unit_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Unit deleted',204

api.add_resource(qry_unit, "/API/units/qry_unit")

class dailydata(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        vartable = ltbfl[ltbfl['id_sec'] == 'ntVariables']
        varfield = ltbfl[ltbfl['id_sec'] == 'ncVariable']
        vtfield = ltbfl[ltbfl['id_sec'] == 'ncTipoDDoDE']
        vnfield = ltbfl[ltbfl['id_sec'] == 'ncNombreTabla']
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstaciones']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        datefield = ltbfl[ltbfl['id_sec'] == 'ncFecha']
        valuefield = ltbfl[ltbfl['id_sec'] == 'ncValor']
        maxvalfield = ltbfl[ltbfl['id_sec'] == 'ncValorMax']
        minvalfield = ltbfl[ltbfl['id_sec'] == 'ncValorMin']
        maxdatefield = ltbfl[ltbfl['id_sec'] == 'ncFechaHoraMax']
        mindatefield = ltbfl[ltbfl['id_sec'] == 'ncFechaHoraMin']
        parser = reqparse.RequestParser()
        parser.add_argument('stn_id')
        parser.add_argument('var_id')
        parser.add_argument('date_ini')
        parser.add_argument('date_end')
        parser.add_argument('datee')
        args = parser.parse_args()
        stn_id = args.get('stn_id')
        var_id = args.get('var_id')
        date_ini = args.get('date_ini')
        date_end = args.get('date_end')
        datee = args.get('datee')
        # query variable table for tablename
        strqry='select * from ' +vartable.iloc[0,1] +' where ' +varfield.iloc[0,1] +'="'+ var_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        datavar = qry.fetchall()
        rcount=qry.rowcount
        extreme = False
        if rcount > 0:
            variable = pd.DataFrame(data=datavar, dtype="string")
            tablename = variable.iloc[0,5] +variable.iloc[0,3]
            if variable.iloc[0,5] == 'DE':
                extreme = True
        else:
            abort(404, message="Variable not found...")
        qry.close
        # check if it is a date or a period 
        if datee in (None, ''):
            if extreme == True:
                strqry='select ' +stnfield.iloc[0,1] + ',' +datefield.iloc[0,1] + ',' +valuefield.iloc[0,1] + ',' +maxdatefield.iloc[0,1] + ',' +maxvalfield.iloc[0,1] + ',' +mindatefield.iloc[0,1] + ',' +minvalfield.iloc[0,1] +' from ' + tablename +' where ' + stnfield.iloc[0,1] +'="'+ str(stn_id) +'" and ' + datefield.iloc[0,1] +'>="' + str(date_ini) +'" and ' + datefield.iloc[0,1] +'<="' + str(date_end) +'"'
            else:
                strqry='select ' +stnfield.iloc[0,1] + ',' +datefield.iloc[0,1] + ',' +valuefield.iloc[0,1] +' from ' + tablename +' where ' + stnfield.iloc[0,1] +'="'+ str(stn_id) +'" and ' + datefield.iloc[0,1] +'>="' + str(date_ini) +'" and ' + datefield.iloc[0,1] +'<="' + str(date_end) +'"'
        else:
            if extreme == True:
                strqry='select '  +stnfield.iloc[0,1] + ',' +datefield.iloc[0,1] + ',' +valuefield.iloc[0,1] + ',' +maxdatefield.iloc[0,1] + ',' +maxvalfield.iloc[0,1] + ',' +mindatefield.iloc[0,1] + ',' +minvalfield.iloc[0,1] +' from ' + tablename +' where ' + stnfield.iloc[0,1] +'="'+ str(stn_id) +'" and ' + datefield.iloc[0,1] +'="' + str(datee) +'"'
            else:
                strqry='select ' +stnfield.iloc[0,1] + ',' +datefield.iloc[0,1] + ',' +valuefield.iloc[0,1] +' from ' + tablename +' where ' + stnfield.iloc[0,1] +'="'+ str(stn_id) +'" and ' + datefield.iloc[0,1] +'="' + str(datee) +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            if extreme == True:
                ddata = pd.DataFrame(data=dataqry,columns=['Station','Date','Value','MaxValDate','MaxValue','MinValDate','MinValue'])
            else:
                ddata = pd.DataFrame(data=dataqry,columns=['Station','Date','Value'])
            jsondata = ddata.to_json(orient="records",date_format='iso', date_unit='s')
            parsed = json.loads(jsondata)
        else:
            abort(404, message="There is no data...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        vartable = ltbfl[ltbfl['id_sec'] == 'ntVariables']
        varfield = ltbfl[ltbfl['id_sec'] == 'ncVariable']
        vtfield = ltbfl[ltbfl['id_sec'] == 'ncTipoDDoDE']
        vnfield = ltbfl[ltbfl['id_sec'] == 'ncNombreTabla']
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstaciones']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        datefield = ltbfl[ltbfl['id_sec'] == 'ncFecha']
        valuefield = ltbfl[ltbfl['id_sec'] == 'ncValor']
        maxvalfield = ltbfl[ltbfl['id_sec'] == 'ncValorMax']
        minvalfield = ltbfl[ltbfl['id_sec'] == 'ncValorMin']
        maxdatefield = ltbfl[ltbfl['id_sec'] == 'ncFechaHoraMax']
        mindatefield = ltbfl[ltbfl['id_sec'] == 'ncFechaHoraMin']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('stn_id')
        parser.add_argument('var_id')
        parser.add_argument('datee')
        parser.add_argument('value')
        parser.add_argument('maxvaldate')
        parser.add_argument('maxvalue')
        parser.add_argument('minvaldate')
        parser.add_argument('minvalue')
        args = parser.parse_args()
        jfile = args.get('file')
        stn_id = args.get('stn_id')
        var_id = args.get('var_id')
        datee = args.get('datee')
        value = args.get('value')
        maxvaldate = args.get('maxvaldate')
        maxvalue = args.get('maxvalue')
        minvaldate = args.get('minvaldate')
        minvalue = args.get('minvalue')
        # query variable table for tablename
        strqry='select * from ' +vartable.iloc[0,1] +' where ' +varfield.iloc[0,1] +'="'+ var_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        datavar = qry.fetchall()
        rcount=qry.rowcount
        extreme = False
        if rcount > 0:
            variable = pd.DataFrame(data=datavar, dtype="string")
            tablename = variable.iloc[0,5] +variable.iloc[0,3]
            if (variable.iloc[0,5] == 'DE' or variable.iloc[0,5] == 'de'):
                extreme = True
        else:
            abort(404, message="Variable not found...")
        qry.close
        # verify if input is a file
        if jfile in (None, ''):
            # check if it is extreme data
            if extreme == True:
                strqry = ('insert ignore into ' +tablename +' values("' +str(stn_id) +'","' +str(datee) +'","' +str(value) + '","",' +str(maxvaldate) +'","' +str(maxvalue) +'",",""' +str(minvaldate) +'","' +str(minvalue) +'","","0","0","0","API")')
            else:
                strqry = ('insert ignore into ' +tablename +' values("' +str(stn_id) +'","' +str(datee) +'","' +str(value) +'","","0","0","0","API")')
            strqry=strqry.lower()
            qry.execute(strqry)
            dataqry = qry.fetchall()
            rcount=qry.rowcount
            qry.close
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows:
                    # check if it is extreme data
                    if extreme == True:
                        strqry = ('insert ignore into ' +tablename +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] + '","",' +data.iloc[int(n),3] +'","' +data.iloc[int(n),4] +'",",""' +data.iloc[int(n),5] +'","' +data.iloc[int(n),6] +'","","0","0","0","API")')
                    else:
                        strqry = ('insert ignore into ' +tablename +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'")')
                    qry.execute(strqry) 
            else:
                # check if it is extreme data
                if extreme == True:
                    strqry = ('insert ignore into ' +tablename +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] + '","",' +data.iloc[0,3] +'","' +data.iloc[0,4] +'",",""' +data.iloc[0,5] +'","' +data.iloc[0,6] +'","","0","0","0","API")')
                else:
                    strqry = ('insert ignore into ' +tablename +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] +'")')
                qry.execute(strqry)       
        return 'Data stored',201 
    def delete(self):
        qry = mysql.connection.cursor()
        vartable = ltbfl[ltbfl['id_sec'] == 'ntVariables']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        datefield = ltbfl[ltbfl['id_sec'] == 'ncFecha']
        parser = reqparse.RequestParser()
        parser.add_argument('stn_id')
        parser.add_argument('var_id')
        parser.add_argument('datee')
        args = parser.parse_args()
        stn_id = args.get('stn_id')
        var_id = args.get('var_id')
        datee = args.get('datee')
                # query variable table for tablename
        strqry='select * from ' +vartable.iloc[0,1] +' where ' +varfield.iloc[0,1] +'="'+ var_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        datavar = qry.fetchall()
        rcount=qry.rowcount
        if rcount > 0:
            variable = pd.DataFrame(data=datavar, dtype="string")
            tablename = variable.iloc[0,5] +variable.iloc[0,3]
        else:
            abort(404, message="Variable not found...")
        qry.close
        strqry='delete from ' +tablename +' where ' +stnfield.iloc[0,1] +'="'+ stn_id +'" and ' +datefield.iloc[0,1] +'="'+ datee +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Record deleted',204      

api.add_resource(dailydata, "/API/data/dailydata")

class detaildata(Resource):
    def get(self):        
        qry = mysql.connection.cursor()
        vartable = ltbfl[ltbfl['id_sec'] == 'ntVariables']
        varfield = ltbfl[ltbfl['id_sec'] == 'ncVariable']
        vtfield = ltbfl[ltbfl['id_sec'] == 'ncTipoDDoDE']
        vnfield = ltbfl[ltbfl['id_sec'] == 'ncNombreTabla']
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstaciones']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        datefield = ltbfl[ltbfl['id_sec'] == 'ncFecha']
        valuefield = ltbfl[ltbfl['id_sec'] == 'ncValor']
        parser = reqparse.RequestParser()
        parser.add_argument('stn_id')
        parser.add_argument('var_id')
        parser.add_argument('date_ini')
        parser.add_argument('date_end')
        parser.add_argument('datee')
        args = parser.parse_args()
        stn_id = args.get('stn_id')
        var_id = args.get('var_id')
        date_ini = args.get('date_ini')
        date_end = args.get('date_end')
        datee = args.get('datee')
        # query variable table for tablename
        strqry='select * from ' +vartable.iloc[0,1] +' where ' +varfield.iloc[0,1] +'="'+ var_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        datavar = qry.fetchall()
        rcount=qry.rowcount
        if rcount > 0:
            variable = pd.DataFrame(data=datavar, dtype="string")
            tablename = 'dt' +variable.iloc[0,3]
        else:
            abort(404, message="Variable not found...")
        qry.close
        # check if it is a date or a period 
        if datee in (None, ''):
            strqry='select ' +stnfield.iloc[0,1] + ',' +datefield.iloc[0,1] + ',' +valuefield.iloc[0,1] +' from ' + tablename +' where ' + stnfield.iloc[0,1] +'="'+ str(stn_id) +'" and ' + datefield.iloc[0,1] +'>="' + str(date_ini) +'" and ' + datefield.iloc[0,1] +'<="' + str(date_end) +'"'
        else:
            strqry='select ' +stnfield.iloc[0,1] + ',' +datefield.iloc[0,1] + ',' +valuefield.iloc[0,1] +' from ' + tablename +' where ' + stnfield.iloc[0,1] +'="'+ str(stn_id) +'" and ' + datefield.iloc[0,1] +'="' + str(datee) +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        dataqry = qry.fetchall()
        rcount=qry.rowcount
        qry.close
        if rcount > 0:
            ddata = pd.DataFrame(data=dataqry,columns=['Station','Date','Value'])
            jsondata = ddata.to_json(orient="records",date_format='iso', date_unit='s')
            parsed = json.loads(jsondata)
        else:
            abort(404, message="There is no data...")
        return parsed
    def post(self):
        qry = mysql.connection.cursor()
        vartable = ltbfl[ltbfl['id_sec'] == 'ntVariables']
        varfield = ltbfl[ltbfl['id_sec'] == 'ncVariable']
        vnfield = ltbfl[ltbfl['id_sec'] == 'ncNombreTabla']
        stntable = ltbfl[ltbfl['id_sec'] == 'ntEstaciones']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        datefield = ltbfl[ltbfl['id_sec'] == 'ncFecha']
        valuefield = ltbfl[ltbfl['id_sec'] == 'ncValor']
        parser = reqparse.RequestParser()
        parser.add_argument('file')
        parser.add_argument('stn_id')
        parser.add_argument('var_id')
        parser.add_argument('datee')
        parser.add_argument('value')
        args = parser.parse_args()
        jfile = args.get('file')
        stn_id = args.get('stn_id')
        var_id = args.get('var_id')
        datee = args.get('datee')
        value = args.get('value')
        # query variable table for tablename
        strqry='select * from ' +vartable.iloc[0,1] +' where ' +varfield.iloc[0,1] +'="'+ var_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        datavar = qry.fetchall()
        rcount=qry.rowcount
        if rcount > 0:
            variable = pd.DataFrame(data=datavar, dtype="string")
            tablename = 'dt' +variable.iloc[0,3]
        else:
            abort(404, message="Variable not found...")
        qry.close
        # verify if input is a file
        if jfile in (None, ''):
            strqry = ('insert ignore into ' +tablename +' values("' +str(stn_id) +'","' +str(datee) +'","' +str(value) +'","' +str(value) +'","","API","0")')
            strqry=strqry.lower()
            qry.execute(strqry)
            dataqry = qry.fetchall()
            rcount=qry.rowcount
            qry.close
        else:
            f=open(jfile,'r')
            filej = f.read()  
            f.close()
            jdata = json.loads(filej)
            data = pd.DataFrame(jdata)
            fields = data.columns.tolist()
            tdata=len(data.index)
            rows=list(range(0,tdata))
            if int(tdata) > 1:
                for n in rows: 
                    strqry = ('insert ignore into ' +tablename +' values("' +data.iloc[int(n),0] +'","' +data.iloc[int(n),1] +'","' +data.iloc[int(n),2] +'","' +data.iloc[int(n),2] +'","","API","0")')
                    qry.execute(strqry) 
            else:
                strqry = ('insert ignore into ' +tablename +' values("' +data.iloc[0,0] +'","' +data.iloc[0,1] +'","' +data.iloc[0,2] +'","' +data.iloc[0,2] +'","","API","0")')
                qry.execute(strqry)       
        return 'Data stored',201
    def delete(self):
        qry = mysql.connection.cursor()
        vartable = ltbfl[ltbfl['id_sec'] == 'ntVariables']
        stnfield = ltbfl[ltbfl['id_sec'] == 'ncEstacion']
        datefield = ltbfl[ltbfl['id_sec'] == 'ncFecha']
        parser = reqparse.RequestParser()
        parser.add_argument('stn_id')
        parser.add_argument('var_id')
        parser.add_argument('datee')
        args = parser.parse_args()
        stn_id = args.get('stn_id')
        var_id = args.get('var_id')
        datee = args.get('datee')
                # query variable table for tablename
        strqry='select * from ' +vartable.iloc[0,1] +' where ' +varfield.iloc[0,1] +'="'+ var_id +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        datavar = qry.fetchall()
        rcount=qry.rowcount
        if rcount > 0:
            variable = pd.DataFrame(data=datavar, dtype="string")
            tablename = 'dt' +variable.iloc[0,3]
        else:
            abort(404, message="Variable not found...")
        qry.close
        strqry='delete from ' +tablename +' where ' +stnfield.iloc[0,1] +'="'+ stn_id +'" and ' +datefield.iloc[0,1] +'="'+ datee +'"'
        strqry=strqry.lower()
        qry.execute(strqry)
        return 'Record deleted',204  

api.add_resource(detaildata, "/API/data/detaildata")

#start server
if __name__ == "__main__":
    app.run(debug=True)
THRESHOLDS = {
    "PM25" : {
        "VERY GOOD" : 25,
        "GOOD" : 37,
        "MODERATE" : 50,
        "BAD" : 90
    },
    "TEMP" : {
        "COLD" : 18,
        "HOT" : 30,
        "EXTREME" : 35
    },
    "HUMIDITY" : {
        "DRY" : 40,
        "WET" : 80
    }
}

def air_condition(pm25_index):
    if(pm25_index < THRESHOLDS['PM25']['VERY GOOD']):
        return 'very good'
    elif(pm25_index < THRESHOLDS['PM25']['GOOD']):
        return 'good'
    elif(pm25_index < THRESHOLDS['PM25']['MODERATE']):
        return 'moderate'
    elif(pm25_index < THRESHOLDS['PM25']['BAD']):
        return 'bad'
    else:
        return 'very bad'

def feeling(temp, humidity):
    # cold weather
    if(temp <= THRESHOLDS['TEMP']['COLD']):
        if(humidity >= THRESHOLDS['HUMIDITY']['WET']):
            return 'cold','wet'
        else:
            return 'cold','dry'
    # hot weather
    if(temp >= THRESHOLDS['TEMP']['HOT']):
        if(humidity >= THRESHOLDS['HUMIDITY']['WET']):
            return 'hot','wet'
        elif(humidity <= THRESHOLDS['HUMIDITY']['WET']):
            return 'hot', 'dry'
        else:
            return 'hot', 'normal'
    # extreme hot
    if(temp > THRESHOLDS['TEMP']['EXTREME']):
        return 'extreme hot'
    # normal weather
    else:
        if(humidity >= THRESHOLDS['HUMIDITY']['WET']):
            return 'normal','wet'
        elif(humidity <= THRESHOLDS['HUMIDITY']['DRY']):
            return 'normal', 'dry'
        else:
            return 'normal','normal'
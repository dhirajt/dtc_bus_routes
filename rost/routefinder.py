from models import Stage, Route, StageSeq


def findroutes(startstage, endstage):
    buses = Route.objects.filter(
                stages__name__icontains=startstage).filter(
                stages__name__icontains=endstage)
    data = {}
    if buses:
        for bus in buses:
            stops = StageSeq.objects.select_related().filter(route__name=bus.name)
            x = stops.get(stage__name__icontains=startstage).sequence
            y = stops.get(stage__name__icontains=endstage).sequence
            stops = stops[min(x, y)-1:max(x, y)]
            data[bus.name] = [it.stage.name for it in stops]
            if data[bus.name][0] != startstage:
                data[bus.name].reverse()
        
        shortest = min(data,key=lambda item:len(data[item]))
        buslist = [shortest] + [ i for i in data.keys() if i!=shortest ]
        return (buses, data, buslist)
    else :
        buses, data, buslist = indirectroutes(startstage,endstage)
        return buses, data, buslist
    
def indirectroutes(startstage,endstage):
    buses_data = Route.objects.values_list('name','stages__name')
    start_buses = Route.objects.filter(stages__name__icontains=startstage).values_list('name',flat=True)
    
    start_bus_dict = {}
    for num, stop in buses_data:
        if num in start_buses:
            if num not in start_bus_dict:
                start_bus_dict[num] = []
            start_bus_dict[num].append(stop)
    return None, None, None

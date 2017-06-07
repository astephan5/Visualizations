import csv
region_names=['England and Wales','North East', 'North West', 'Yorkshire and The Humber', 'East Midlands', 'West Midlands', 'East', 'London', 'South East', 'South West', 'Wales']
region_coords=[(500,650),(320,100), (280,150), (370,200), (400,300), (300,350), (500,350), (450,420), (400,450), (190,500), (220,400)]
name_dict=dict(zip(region_names, region_coords))
quarters=['Q1', 'Q2', 'Q3', 'Q4']
years=[]
for i in range(1995, 2017):
    for q in quarters:
        s=str(q)+'-'+str(i)
        years.append(s)
years=years[3:86]
class Region(object):
    def __init__(self, name, data, time_point, scl):
        self.data=data
        self.name=name
        self.time_point=time_point
        self.detached={}
        self.semi_detached={}
        self.flats={}
        self.scl=scl
    def render(self):
        x=name_dict[self.name][0]
        y=name_dict[self.name][1]
        total=float(self.data[self.time_point].replace(',', ''))
        b_factor=float(self.detached[self.time_point].replace(',', ''))
        r_factor=float(self.flats[self.time_point].replace(',', ''))
        total_color=r_factor+b_factor
        r=r_factor/total*255
        b=b_factor/total*255
        self.diam=15*total/(self.scl*float(5000))
        fill(r,0,b)
        ellipse(x,y,self.diam,self.diam)
        fill(0)
        textSize(14)
        if self.name=="England and Wales":
            text(self.name, x-50, y-50)
        else:
            text(self.name, x, y+20)
def setup():
    size(612,620)
    smooth()
def update_tick():
    textSize(6)
    textAlign(LEFT,TOP)
    fill(255)
    tick=millis()/1000
    text("Time: %.2f" % tick,3,3)
    return tick
def draw():
    img=loadImage('england5.png')
    image(img, 0, 0, 612, 600)
    tick=update_tick()
    for j in range(0,51):
        x=12*j
        y=590
        fill(255-5*j, 0, 0+5*j)
        rect(x,y,12,30)
    textSize(18)
    fill(0)
    text("More Flats", 0, 570)
    text("More Detached", 475, 570)
    regions=[]
    with open("overall.csv") as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            d=row
            if row['Name']=='England and Wales':
                s=5
            else:
                s=1
            r=Region(row['Name'], d, 'Q4-1995', s)
            regions.append(r)
    with open("detached.csv") as csvfile2:
        reader=csv.DictReader(csvfile2)
        for row in reader:
            for region in regions:
                if row['Name']==region.name:
                    region.detached=row
    with open("semi-detached.csv") as csvfile3:
        reader=csv.DictReader(csvfile3)
        for row in reader:
            for region in regions:
                if row['Name']==region.name:
                    region.semi_detached=row
    with open("flats.csv") as csvfile4:
        reader=csv.DictReader(csvfile4)
        for row in reader:
            for region in regions:
                if row['Name']==region.name:
                    region.flats=row
    times=list(range(0, 83))
    x=0
    for time in times:
        if tick>=time and tick<=x:
            fill(0)
            textSize(24)
            text(years[time], 450, 20)
            for region in regions[1:]:
                region.time_point=years[time]
                region.render()
        x=x+1
    #saveFrame()
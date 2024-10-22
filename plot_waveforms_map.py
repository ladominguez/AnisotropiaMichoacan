import pygmt
import os
from obspy import read
import numpy as np
import geopy.distance
from matplotlib import pyplot as plt
import glob


root = '/Users/antonio/SynologyDrive/Research/Anisotropy/Tancitaro'
titles = {
'2024-08-02T22:23:02' : 'Philippines',
'2024-06-14T04:26:48' : 'South Atlantic',
'2024-05-25T22:23:16' : 'Vanuatu',
'2024-07-22T05:04:30' : 'Vanuatu',
'2024-08-15T23:35:53' : 'Taiwan',
'2024-08-08T07:42:55' : 'Kyushu, Japan',
'2024-07-07T20:01:12' : 'Japan',
'2024-08-10T03:28:32' : 'Sajalin, Russia',
'2024-05-31T15:54:41' : 'Tonga',
'2024-09-01T20:13:34' : 'Salomon',
'2024-06-16T00:27:57' : 'Antartica - New Zeland',
'2024-09-05T01:03:15' : 'Papua New Guinea',
'2024-05-08T08:17:18' : 'Vanuatu',
'2024-07-11T02:13:17' : 'Philippines',
'2024-07-10T04:55:41' : 'Antartica South Africa',
'2024-08-03T04:20:26' : 'Philippines',
'2024-05-05T18:33:10' : 'Banda Sea'
}

def plot_map(sac_files, evdp):
    verticals = sac_files.select(channel='HHZ')
    time = verticals[0].stats.starttime.strftime('%Y-%m-%dT%H:%M:%S')

    array_lat = np.mean(np.array([vertical.stats.sac.stla for vertical in verticals]), axis=0)
    array_lon = np.mean(np.array([vertical.stats.sac.stlo for vertical in verticals]), axis=0)
    mean_dist = np.mean(np.array([vertical.stats.sac.dist for vertical in verticals]), axis=0)
    mean_gcarc = np.mean(np.array([vertical.stats.sac.gcarc for vertical in verticals]), axis=0)
    mean_baz = np.mean(np.array([vertical.stats.sac.baz for vertical in verticals]), axis=0)
    array_location = (array_lat, array_lon)
    #print('Mean distance', mean_dist)

    mid_point = geopy.distance.distance(kilometers=mean_dist/2).destination(array_location, bearing=mean_baz)

    projection = f'A{mid_point[1]}/{mid_point[0]}/130/10c'
    #print('Projection', projection)
    #projection="A30/-20/60/12c"
        
    fig = pygmt.Figure()
    fig.coast(region='g', projection=projection, frame='afg', land='gray69', water='lightblue')
    fig.basemap(frame=[fr"+t{titles[time]} Mw{mag}+s {time} depth = {evdp:.1f} km"])
    fig.plot(x=[evlo, array_lon], y=[evla, array_lat], pen='black')
    fig.text(x=mid_point.longitude, y=mid_point.latitude, text=fr'@[d={mean_gcarc:4.1f}^o@[', font='12p,Helvetica,black')
    fig.plot(x=array_lon, y=array_lat, style='c0.2c', fill='red', pen='black')
    fig.plot(x=evlo, y=evla, style='c0.2c', fill='blue', pen='black')
    fig.savefig(f'{directory_path}/{time}_{titles[time].replace(' ','')}_map.png', dpi=300)


def get_directory_path(root, date):
    directory_and_files = glob.glob(os.path.join(root, date + '*'))
    if len(directory_and_files) == 0:
        return None
    path_directory = [d for d in directory_and_files if os.path.isdir(d)]
    return path_directory[0]    

def plot_waveforms(stream, evdp,zoom=False):
    stream.detrend('demean')
    stream.detrend('linear')
    stream.taper(max_percentage=0.05, type='cosine')
    stream.filter('bandpass', freqmin=0.02, freqmax=0.1, corners=2, zerophase=True)
    stations = set([tr.stats.sac.kstnm for tr in stream])

    for station in stations:
        vertical = stream.select(station=station, channel='HHZ')
        east = stream.select(station=station, channel='HHE')
        north = stream.select(station=station, channel='HHN')
        radial = stream.select(station=station, channel='HHR')
        transverse = stream.select(station=station, channel='HHT')


        t0 = vertical[0].stats.sac.t0
        time_sac = vertical[0].times()
        if zoom:
            indices = np.where((time_sac > t0 - 60) & (time_sac < t0 + 200))
            time_sac = time_sac[indices]
            fig, ax = plt.subplots(5, 1, figsize=(5, 8), sharex=True, sharey=True)
            lw = 2;
        else:
            indices = np.where((time_sac >= np.min(time_sac)) & (time_sac <= np.max(time_sac))) 
            fig, ax = plt.subplots(5, 1, figsize=(12, 8), sharex=True, sharey=True)
            lw = 0.25
        
        fig.subplots_adjust(hspace=0)
    
        time = vertical[0].stats.starttime.strftime('%Y-%m-%dT%H:%M:%S')
        ax[0].plot(time_sac, vertical[0].data[indices],'k', linewidth=lw, label='Vertical')
        #ax[0].suptitle(f'{titles[time]} Mw{mag}')
        ax[0].set_title(f'{date} {titles[time]} Mw{mag} \nstation: {station} $d={vertical[0].stats.sac.gcarc:4.1f}^o$ depth = {evdp:.1f} km')
        ax[0].annotate('Vertical', xy=(0.05, 0.8), xycoords='axes fraction', fontsize=14)
        ax[0].axvline(t0, color='red', linestyle='--')
        ax[0].annotate('SKS', xy=(t0, 0.8*np.max(np.abs(vertical[0].data))), xycoords='data', fontsize=14)
        ax[1].plot(time_sac, east[0].data[indices],'k', linewidth=lw, label='East')
        ax[1].annotate('East', xy=(0.05, 0.8), xycoords='axes fraction', fontsize=14)
        ax[1].axvline(t0, color='red', linestyle='--')
        ax[2].plot(time_sac, north[0].data[indices], 'k', linewidth= lw,label='North')
        ax[2].annotate('North', xy=(0.05, 0.8), xycoords='axes fraction', fontsize=14)
        ax[2].axvline(t0, color='red', linestyle='--')
        ax[3].plot(time_sac, radial[0].data[indices], 'k', linewidth=lw, label='Radial')
        ax[3].annotate('Radial', xy=(0.05, 0.8), xycoords='axes fraction', fontsize=14)
        ax[3].axvline(t0, color='red', linestyle='--')
        ax[4].plot(time_sac, transverse[0].data[indices],'k', linewidth= lw,  label='Transverse')
        ax[4].axvline(t0, color='red', linestyle='--')
        ax[4].annotate('Transverse', xy=(0.05, 0.8), xycoords='axes fraction', fontsize=14)
        ax[4].set_xlabel('Time [s]')
        if zoom:
            ax[4].set_xlim(t0-60, t0+200)
            fileout = os.path.join(directory_path, f'{date}_{station}_zoom.png')
        else:
            ax[4].set_xlim(np.min(time_sac), np.max(time_sac))
            fileout = os.path.join(directory_path, f'{date}_{station}.png')

        
        fig.savefig(fileout, dpi=300)
        
        print('Saving', fileout)
        plt.close(fig)

if __name__ == '__main__':

    with open('catalog_Tancitaro.txt') as f:
        lines = f.readlines()

    for line in lines:
        print(line.strip())
        mag  = float(line.split()[1])
        evla = float(line.split()[2])
        evlo = float(line.split()[3])
        evdp = float(line.split()[4])
        date = line.split()[0]

        eq_location = (evla, evlo)

        path_sac_files = os.path.join(root,date + '*', '*.sac')

        try:
            stream = read(path_sac_files)
            
        except:
            print('No files found in ', path_sac_files)
            continue

        directory_path = get_directory_path(root, date)
        print('Directory path', directory_path)

        stream_copy = stream.copy()

        plot_map(stream, evdp)
        plot_waveforms(stream, evdp, zoom=False)
        plot_waveforms(stream_copy, evdp, zoom=True)

    


        
        
        

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

ttk.Label(tab1,
          text="Welcome to GeeksForGeeks").grid(column=0,
                               row=0,
                               padx=30,
                               pady=30)
ttk.Label(tab2,
          text="Lets dive into the world of computers").grid(column=0,
                                    row=0,
                                    padx=30,
                                    pady=30)

root.mainloop()
# bfs = BFSTrigger()
# bfs.cam.Init()
# st = time.time()
# bfs.getDeviceParams()
# print(bfs.CamProperties)
# print(time.time() - st)
# bfs.cam.DeInit()
# system = PySpin.System_GetInstance()
# cam = system.GetCameras()[0]
# cam.Init()
# st = time.time()
# #print('Time to init: %f seconds' % (time.time() - st))
# if cam.TLDevice.DeviceSerialNumber.GetAccessMode() == PySpin.RO:
#     print('Device serial number: %s' % cam.TLDevice.DeviceSerialNumber.ToString())
#
# # Print device display name
# if PySpin.IsReadable(cam.TLDevice.DeviceDisplayName):
#     print('Device display name: %s' % cam.TLDevice.DeviceDisplayName.ToString())
#
# print('Time to print Device serial info: %f seconds' % (time.time() - st))
#
#
# if cam.ExposureTime.GetAccessMode() == PySpin.RO or cam.ExposureTime.GetAccessMode() == PySpin.RW:
#         print('Exposure time: %s' % cam.ExposureTime.ToString())
# else:
#     print('Exposure time: unavailable')
#     result = False
#
# # Print black level
# if PySpin.IsReadable(cam.BlackLevel):
#     print('Black level: %s' % cam.BlackLevel.ToString())
# else:
#     print('Black level: unavailable')
#     result = False
#
# # Print height
# if PySpin.IsReadable(cam.Height):
#     print('Height: %s' % cam.Height.ToString())
# else:
#     print('Height: unavailable')
#     result = False
#
# if PySpin.IsReadable(cam.Gain):
#     print('Gain: %s' % cam.Gain.ToString())
# else:
#     print('gain: unavailable')
#     result = False
#
# if PySpin.IsReadable(cam.Gamma):
#     print('Gamma: %s' % cam.Gamma.ToString())
# else:
#     print('Height: unavailable')
#     result = False
# print('Time to print Device params: %f seconds' % (time.time() - st))
#
# cam.DeInit()
# print('Time to deinit(): %f seconds' % (time.time() - st))


# st = time.time()
# system = PySpin.System.GetInstance()
# cam = system.GetCameras()[0]
# bfs = BFSCam(cam)
# bfs.liveOut()
# print('Took %f  seconds' % (time.time()-st))


# today = date.today()
# owd = os.getcwd()
# h5filepath = 'datafiles/'+today.strftime("%b-%d-%Y")
# os.chdir(h5filepath)
# # for i in range(10):
# #     h5m.createFile('shot' + '0'*(4-len(str(i+1))) + str(i+1) + '.hdf5')
# dirs = os.listdir()
# dirs.sort(reverse=True)
# lastfile = dirs[0]
# lf1 = lastfile[:-5].split('shot')[1]
# for i in range(len(str(lf1))):
#     if lf1[i] != '0':
#         filenum = lf1[i:]
#         break
#
# print(filenum)
#
#
#

# open('Config/startup.txt')




# plt.rc('font', size=16)          # controls default text sizes
# plt.rc('axes', titlesize=20)     # fontsize of the axes title
# plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
# plt.rc('xtick', labelsize=16)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=16)    # fontsize of the tick labels
# plt.rc('legend', fontsize=16)    # legend fontsize
# plt.rc('figure', titlesize=20)  # fontsize of the figure title
# plt.rc("lines", lw=2, markersize=8)
# plt.rcParams["axes.edgecolor"] = "black"
# plt.rcParams["axes.linewidth"] = 1
# plt.rcParams["axes.edgecolor"] = "0.3"
# plt.rcParams["figure.facecolor"] = "w"

# with h5py.File("20200806_115841_testShot_Shot00012.h5", 'r', libver='earliest') as f:
#     b = f.get('s')
#     print(b.items())
#     print(f.attrs.keys())
#     # print(f['s']['index'])
#     # img = f['s']["Camera 1 - Images"][0]

# import tkinter as tk
#
#
# def display_entry(event):
#     output['text'] += "\n" + entry.get()
#     entry.delete(0, tk.END)
#
#
# root = tk.Tk()
# root.geometry('500x500')
#
# entry = tk.Entry(root)
# entry.pack(side=tk.BOTTOM, fill=tk.X)
# entry.bind('<Return>', display_entry)
#
# output = tk.Label(root, background='#a0ffa0', anchor=tk.W, justify=tk.LEFT)
# output.pack(side=tk.BOTTOM, fill=tk.X)
#
# root.mainloop()


# matrix1 = np.random.random(size= (1000, 1000))
# matrix2 = np.random.random(size= (10000, 100))

# md = {}
# with open('ExFileMetadata.txt', 'r') as f:
#     for i in f.readlines():
#         j = i.rstrip().split(';')
#         md[j[0]] = j[1]
# file = 'h5files/testshot001.hdf5'
#
# h5m.createFile(file)

# for i in range(10):
#     name = 'Param00'+str(i+1)
#     h5m.createDataset(file, name, np.random.random((5, 3, 2, 4, 1)))
#     for key, val in md.items():
#         h5m.setMetadata(file, key, np.random.rand(), path='/' + name)
# h5m.tree(file)





#
# for key, val in md.items():
#     print(key, '->', val)


# shotnum = 1
# # toStore = [1234, 1.234, '5678']
# hdf5_store = HDF5File(file)
# paramnum = 1
#
# for i in range(10):
#     hdf5_store.createGroup('shot' + str(shotnum))
#     for j in range(10):
#         hdf5_store.createDataset('shot'+str(shotnum), 'param'+str(paramnum),
#                                  (10, 20, 3))
#         hdf5_store.append('shot'+str(shotnum), 'param'+str(paramnum),
#                           np.random.random((10, 20, 3)))
#         hdf5_store.append('shot'+str(shotnum), 'param'+str(paramnum),
#                           np.random.random((10, 20, 3)))
#         paramnum += 1
#     shotnum += 1
#     paramnum = 1
# #
# hdf5_store.setMetadata('title', 'updated metadata')
# hdf5_store.setMetadata('time', time.asctime())
#
# #
# with h5py.File(file, 'a') as h5f:
#     # print(list(h5f.keys()))
#     h5f['/'].attrs['test again'] = 'true!'
#     print(list(h5f['/'].attrs.items()))
#     print(list(h5f['shot1'].attrs.items()))
#




# for i in range(100):
#     t = []
#     for j in range(2):
#         t.append(np.random.random())
#     hdf5_store.append(t)



# t = np.linspace(0, 4 * np.pi, 10000)
# a = 10
# b = 0.1
# c = 4.8
# x = 2*((a - b) * np.cos(t) + c * np.cos(((a - b) / b) * t))
# y = 2*((a - b) * np.sin(t) + c * np.sin(((a - b) / b) * t))
#
# with open('g.txt', 'w') as f:
#     f.write('G21 G90\n')
#     for i in range(len(t)):
#         f.write(
#             'G0 X' + str(x[i]) + ' Y' + str(y[i]) + '\n'
#         )


# currentline, t, filename = np.load('temp.npy')
# print(currentline)
# '''
# Sent: G0 X11.749503648982355 Y7.113395302280427
# '''


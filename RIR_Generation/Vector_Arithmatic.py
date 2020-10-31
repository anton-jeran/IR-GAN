import matlab.engine
import tensorflow as tf
import cv2
from IPython.display import display, Audio
import numpy as np 
import librosa
eng = matlab.engine.start_matlab()
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

tf.reset_default_graph()
saver = tf.train.import_meta_graph('infer.meta')
graph = tf.get_default_graph()
sess = tf.InteractiveSession()
saver.restore(sess, 'model.ckpt')

#Set Upper and Lower Limit of DRR
DRR_Upper = 0.0
DRR_Lower = -15.5

#No of intermediate RIRs
Count =600




sample_n=774

Latent_min =0
Latent_max =0
N1 =0
N2 = 0
L =0
RT_L=0
RT_H =100
DRR1=0
DRR2=0
while(L<2):
	# Create 50 random latent vectors z
	_z = (np.random.rand(1000, 100) * 2.) - 1
	# Synthesize G(z)
	z = graph.get_tensor_by_name('z:0')
	G_z = graph.get_tensor_by_name('G_z:0')
	_G_z = sess.run(G_z, {z: _z})
	for i in range (1000):
		wav=_G_z[i][0:16000]
		
		name='sample.wav'
		librosa.output.write_wav(path=name,y=wav,sr=16000)
		IrStat = eng.iosr.acoustics.irStats(name,nargout=5)
		RT60 = IrStat[0]
		DRR = IrStat[1]
		CTE = IrStat[2]
		EDT = IrStat[4]
		if(DRR<DRR_Lower and N1<1): 
			if(RT60>RT_L and RT60<RT_H):
				Latent_min = _z[i]
				name = 'v0.wav'
				librosa.output.write_wav(path=name,y=wav,sr=16000)
				N1 =1
				print('DRR : ',DRR)
				print('Latent_min : ',Latent_min)
				RT_L = RT60-0.05
				RT_H = RT60+0.05
				DRR1 =DRR
		if(DRR>DRR_Upper and N2 <1): 
			if(RT60>RT_L and RT60<RT_H): 
				Latent_max = _z[i]
				name = 'v10.wav'
				librosa.output.write_wav(path=name,y=wav,sr=16000)
				N2 =1
				print('DRR : ',DRR)
				print('Latent_max : ',Latent_max)
				RT_L = RT60-0.05
				RT_H = RT60+0.05
				DRR2=DRR
	L = N1+N2

#Finding Gradient Along the Path
grad = (Latent_max - Latent_min)/Count

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
fig2 = plt.figure()
ims=[]
start =0



for n in range(Count):
	_z = Latent_min + (grad*n)
	_z = np.reshape(_z,(1,100))
	# Synthesize G(z)
	z = graph.get_tensor_by_name('z:0')
	G_z = graph.get_tensor_by_name('G_z:0')
	_G_z = sess.run(G_z, {z: _z})
	wav=_G_z[0][0:16000]
	name = 'vect.wav'
	librosa.output.write_wav(path=name,y=wav,sr=16000)
	IrStat = eng.iosr.acoustics.irStats(name,nargout=5)
	RT60 = IrStat[0]
	DRR = IrStat[1]
	CTE = IrStat[2]
	EDT = IrStat[4]
	print("DRR ", DRR)
	title_name = 'Generated Room Impulse Response'
	plt.ylabel("Amplitude")
	plt.xlabel("Time")
	plt.title(title_name)
	Time = np.linspace(0, len(wav) / 16000, num=len(wav))
	Labels = 'DRR : '+ str(DRR)
	ims.append(plt.plot(Time,wav,  label=Labels,color='blue'))



im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
                                   blit=True)
im_ani.save('Vector_Arithmatic_Example.mp4', writer=writer)











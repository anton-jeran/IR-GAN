import matlab.engine
import tensorflow as tf
from IPython.display import display, Audio
import math
import os
import numpy as np 
import librosa
eng = matlab.engine.start_matlab()

tf.reset_default_graph()
saver = tf.train.import_meta_graph('infer.meta')
graph = tf.get_default_graph()
sess = tf.InteractiveSession()
saver.restore(sess, 'model.ckpt')


#The number of augmented data to be generated
augment_sum = 1000

#Directory pointing to real RIRs
directory = '../RIR/'
entries = os.listdir(directory) 


#Reverberation
bin_NRT =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
bin_RT =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
NRT_start =0.6
NRT_width =0.05
NRT_size =36

#Direct to Reverberant Ratio
bin_NDRR =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bin_DRR =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
NDRR_start =-18
NDRR_width =2
NDRR_size =16

#Early to Late Index
bin_NCTE =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bin_CTE =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
NCTE_start =-5
NCTE_width =1
NCTE_size =27

#Early Decay TIme
bin_NEDT =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bin_EDT =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
NEDT_start =0
NEDT_width =0.1
NEDT_size =16

sample_n = 0
print("Learning the distribution of real RIRs")
for name in entries:
	# print("Name ",name)
	file = directory +name
	IrStat = eng.iosr.acoustics.irStats(file,nargout=5)
	RT60 = IrStat[0]
	DRR = IrStat[1]
	CTE = IrStat[2]
	EDT = IrStat[4]	
	for i in range(NRT_size):
		if((RT60>=(NRT_start+(NRT_width*i))) and (RT60<(NRT_start+(NRT_width*(i+1))))):	
			for j in range(NDRR_size):
				if((DRR>=(NDRR_start+(NDRR_width*j))) and (DRR<(NDRR_start+(NDRR_width*(j+1))))):							
					for k in range(NCTE_size):
						if((CTE>=(NCTE_start+(NCTE_width*k))) and (CTE<(NCTE_start+(NCTE_width*(k+1))))):				
							for l in range(NEDT_size):
								if((EDT>=(NEDT_start+(NEDT_width*l))) and (EDT<(NEDT_start+(NEDT_width*(l+1))))):
									sample_n = sample_n+1
									bin_NRT[i] = bin_NRT[i]+1
									bin_NDRR[j] = bin_NDRR[j]+1
									bin_NCTE[k] = bin_NCTE[k] +1	
									bin_NEDT[l] = bin_NEDT[l] +1


sample_ratio = math.ceil((augment_sum/sample_n)*1.5)
print("IR Statistics Distribution of real RIR")
bin_NRT=[element * math.ceil(sample_ratio) for element in bin_NRT]
bin_NDRR=[element * math.ceil(sample_ratio) for element in bin_NDRR]
bin_NCTE=[element * math.ceil(sample_ratio) for element in bin_NCTE]
bin_NEDT=[element * math.ceil(sample_ratio) for element in bin_NEDT]
print("RT Distribution : ", bin_NRT)
print("DRR Distribution : ", bin_NDRR)
print("CTE Distribution : ", bin_NCTE)
print("EDT Distribution : ", bin_NEDT)


sample_n=0


while(sample_n<augment_sum):

	# Create 50 random latent vectors z
	_z = (np.random.rand(1000, 100) * 2.) - 1

	z = graph.get_tensor_by_name('z:0')
	G_z = graph.get_tensor_by_name('G_z:0')
	_G_z = sess.run(G_z, {z: _z})

	for i in range (1000):
		wav=_G_z[i][0:16000]
		name = str(sample_n)+'.wav'
		librosa.output.write_wav(path=name,y=wav,sr=16000)

		IrStat = eng.iosr.acoustics.irStats(name,nargout=5)
		RT60 = IrStat[0]
		DRR = IrStat[1]
		CTE = IrStat[2]
		EDT = IrStat[4]

		for i in range(NRT_size):
			if(bin_RT[i]<bin_NRT[i]):
				if((RT60>=(NRT_start+(NRT_width*i))) and (RT60<(NRT_start+(NRT_width*(i+1))))):	
					for j in range(NDRR_size):
						if(bin_DRR[j]<bin_NDRR[j]):
							if((DRR>=(NDRR_start+(NDRR_width*j))) and (DRR<(NDRR_start+(NDRR_width*(j+1))))):			
								for k in range(NCTE_size):
									if(bin_CTE[k]<bin_NCTE[k]):
										if((CTE>=(NCTE_start+(NCTE_width*k))) and (CTE<(NCTE_start+(NCTE_width*(k+1))))):				
											for l in range(NEDT_size):
												if(bin_EDT[l]<bin_NEDT[l]):
													if((EDT>=(NEDT_start+(NEDT_width*l))) and (EDT<(NEDT_start+(NEDT_width*(l+1))))):
														sample_n = sample_n+1
														bin_RT[i] = bin_RT[i]+1
														bin_DRR[j] = bin_DRR[j]+1
														bin_CTE[k] = bin_CTE[k] +1	
														bin_EDT[l] = bin_EDT[l] +1
														print("sample : ",sample_n)		
														print("target RT Distribution : ", bin_NRT)
														print("current RT Distribution: ", bin_RT)
														print("target DRR Distribution : ", bin_NDRR)
														print("current DRR Distribution : ", bin_DRR)
														print("target CTE Distribution : ", bin_NCTE)
														print("current CTE Distribution : ", bin_CTE)
														print("target EDT Distribution : ", bin_NEDT)
														print("current EDT Distribution : ", bin_EDT)







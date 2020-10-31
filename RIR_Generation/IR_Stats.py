import matlab.engine
import tensorflow as tf
import os
from IPython.display import display, Audio
import numpy as np 
import librosa
eng = matlab.engine.start_matlab()

#Directory pointing to real RIRs
directory = '../RIR/'
entries = os.listdir(directory) 




sample_n=0


#Reverberation
bin_NRT =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
NRT_start =0.6
NRT_width =0.05
NRT_size =36

#Direct to Reverberant Ratio
bin_NDRR =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
NDRR_start =-18
NDRR_width =2
NDRR_size =16

#Early to Late Index
bin_NCTE =    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
NCTE_start =-5
NCTE_width =1
NCTE_size =27

#Early Decay TIme
bin_NEDT =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
NEDT_start =0
NEDT_width =0.1
NEDT_size =16


for name in entries:
	print("Name ",name)
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
									print("sample : ",sample_n)		
									print("RT  Distribution : ", bin_NRT)
									print("DRR Distribution  : ", bin_NDRR)
									print("CTE Distribution  : ", bin_NCTE)
									print("EDT Distribution  : ", bin_NEDT)








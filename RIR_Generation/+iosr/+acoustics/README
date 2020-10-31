This series of M-files generates A-weigthing, C-weighting, octave and
one-third-octave digital filters. These filters are commonly used in
acoustics, for example, in noise control.

The implementation is based on the following standards: 

	* IEC/CD 1672: Electroacoustics-Sound Level Meters, IEC, Geneva, Nov. 1996, 
		for A- and C-weighting filters.

	* ANSI S1.1-1986 (ASA 65-1986): Specifications for Octave-Band 
	  and Fractional-Octave-Band Analog and Digital Filters, ASA, New York, 1993, 
		for octave and one-third-octave filters. 

The following M-files are available:

	octave.tar.gz 	Compressed Unix tar archive containing all of the files below.
	README  	This file. 
	adsgn.m		Design of a A-weighting filter.
	aspec.m     	Plots a filter characteristics vs. A-weighting specifications.
	cdsgn.m		Design of a A-weighting filter.
	cspec.m     	Plots a filter characteristics vs. C-weighting specifications.
	octdsgn.m   	Design of an octave filter.
    	octspec.m   	Plots an octave filter characteristics.
	oct3dsgn.m	Design of a one-third-octave filter.
	oct3spec.m 	Plots a one-third-octave filter characteristics.
	oct3bank.m  	Simple one-third-octave filter bank.
   	filtbank.m    	One-third-octave band frequency analyser.
        leq.m        	Computes the sequence of short-time RMS powers (Leq) of a signal.	
	bankdisp.m      Display filterbank power spectrum in 'bar' form.

The M-files have been tested under MATLAB 4.1 and MATLAB 5.1. 
They should normally work under both versions of MATLAB if you disregard 
the warnings that might be issued in some cases. If it is necessary 
to make changes to a M-file to allow it to work with different versions
of MATLAB, just uncomment the adequate lines of code (alternate code
is provided in the M-file). 

-- Christophe Couvreur (couvreur@thor.fpms.ac.be), August 1997.  


Sample utilisations of the M-files: 
----------------------------------

1) Conception of an A-weighting filter and verification of its characteristics:

	>> Fs = 44100;
	>> [B,A] = adsgn(Fs);
	>> aspec(B,A,Fs); 

2) Conception of a one-third-octave filter and verification of its characteristics:

	>> Fs = 44100;
	>> Fc = 4000; 
	>> [B,A] = oct3dsgn(Fc,Fs);
	>> oct3spec(B,A,Fs,Fc,'ansi'); 

3) Construction of an octave or one-third-octave filter bank:

	See the simple implementation (fixed sampling frequency) in OCT3BANK. 
	Note that a multirate implementation is used to avoid problems
	with the low frequency bands. 

4) Analysis of a signal with FILTBANK: computation of time-varying A-weighted 
   one-third-octave Leq spectrum and display as a waterfall plot. 
   It is assumed that the signal is stored in the variable x. 
   The frame length for the analysis is T = 100ms.
   
	>> Fs = 48000;
	>> T = 100e-3;
	>> [B,A] = adsgn(Fs); 
	>> x = filter(B,A,x); 
	>> [P,F] = filtbank(x,Fs,T,'extended');
	>> waterfall(P');
	>> zlabel('Level [dB]');
	>> ylabel('Frame #');
	>> xlabel('Frequency band');
	>> set(gca,'XTick',[2:3:length(F)]);
	>> set(gca,'XTickLabel',F(2:3:length(F)));


Contact & Comments: 
------------------

   Dr Ir Christophe Couvreur 
   Research Assistant, Belgian National Fund for Scientific Research
   Department of Physics
   Faculte Polytechnique de Mons               
   Rue de Houdain 9                            Ph.  +32 65 374042
   B-7000 Mons (Belgium)                       FAX  +32 65 374045
   E-mail: Christophe.Couvreur@fpms.ac.be
   WWW: http://thor.fpms.ac.be/~couvreur/









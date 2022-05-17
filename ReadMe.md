<h1>Music Generation</h1>

This is an implementation of evolutionary algorithm for music generation based on paper:
Kowalczuk Z., Tatara M., Bąk A. (2017). Evolutionary music composition system with statistically modeled criteria. *Advances in Intelligent Systems and Computing*"

To generate new music run <b>generate_music.py</b>. 
In that file you can also modify following parameters:

- population size
- song size
- tonality
- number of epochs



To listen to generated music run <b>play_music.py</b>. It will also save currently played music to .mid file.



If you want to change the weights of various statistical features used in the fitness function - you can do so in the  <b>evolution/features.py</b>. 


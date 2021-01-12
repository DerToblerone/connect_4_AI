# connect_4_AI
Attempt to create a connect 4 AI using neural networks using keras and tensorflow

To run this code you need to install the keras and tensorflow libraries, as well as numpy.

File descriptions:
  
* **net_vs_net.py**  
    This file loads two saved networks and lets them play 20 games against each other. The  
    results are then saved in a .txt file.
    
 * **opp_test.py**   
    You can use this file to play against non-neural network opponents. By changing the parameters of  
    the play() function at the end, you can play human vs human, human vs CPU or CPU vs CPU.
   
 * **oppo.py**  
    Contains the three non-network player classes. Human, random and random rollout. random rollout can accept  
    an integer parameter, if one is given, it determines the number of random game playouts (rollouts) per legal move.
    
 * **play_network.py**  
    Lets you play against a network.
    
 * **predict_util.py**  
    Contains functions that handle move evaluation for the network.
    
  * **test_network.py**  
    Lets you test the networks strength against several CPU opponents. The results are then saved into a .txt file.
   
  * **train_generated_data.py**  
    This trains a network with data generated by CPU players of varying strength. Then the Network uses the generated  
    games to train. the value of a move is determined by the outcome of the game and can either be  
    0(X lost or draw) or 1 (X won).
    
  * **train_TD.py**  
    This network trains differently using a TD method and through self play (and playing against CPU opponents).
  
  * **util.py**  
    Contains several functions handeling output display, playing moves and converting board representations.
    
  * **win.py**  
    Contains a function to determine the winner of a connect 4 game.
    
### Training recommendations:  
A network with 30 hidden neurons seems to produce decent results. In the training_generated_data.py file, a network  
like this is trained with 10000 generated games (takes quite long on my pc) for 50 epochs. On my setup it achieved the  
following winrate(RNG = random opponent, RX = random_rollout with parameter X:  
  
w:  19  l:  1   d:  0   RNG  
w:  15  l:  4   d:  1   R50  
w:  8   l:  11  d:  1   R250  
w:  13  l:  7   d:  0   R500  

It is surprising that it lost against RNG, but it performed quite well against the other machine opponents.

As comparison, a network with 60 hidden neurons that trained via TD achived the following score:

w:  20  l:  0   d:  0   RNG  
w:  9   l:  9   d:  2   R50  
w:  1   l:  17  d:  2   R250  
w:  0   l:  15  d:  5   R500  

Even though it was less strong against the rollout opponents, the two networks playing against each other resulted in a score of  
10 to 10. 



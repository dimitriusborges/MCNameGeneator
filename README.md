## MCNameGeneator

  ## **Description**
    This simple code emulates the principles of a Markov Chain to generate random names seeded from a database.

  ## **Limitations**
    This first version requires single names, with no accents or especial characters, written in roman alphabet. 
    
 ## **Configuration**
  - The Database is represented by a .txt external file, indicated through its real path. 
  - Three configurable variables are used:
    - _max_size_ = The max number of letters allowed
    - _total_gen_ = Number of names generated in one execution
    - _st_size_ = Size of the states, i.e., the number of letters each state must have. 
    However, if the size of a given name divided by st_size does not give an exact result, the code will generated states with a different size. 

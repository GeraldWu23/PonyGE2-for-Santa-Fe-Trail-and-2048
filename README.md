## PonyGE2 on Santa Fe Trail and 2048

this is a GE system with which we can generate a programme to solve Santa Fe Trail or 2048 automatically.



1. Create a document called 'PythonCode' under disk (D:) and put the whole project file(PonyGE2-master) in it. This step makes sure the environment setting is the same as that in my computer.

2. Make sure your python version is 3.5 or after that. 

3. Open command processor, change your directory to D:\PythonCode\PonyGE2-master\src>

4. If you have both Python2 and Python3 in your computer, make sure Python3 is activated, in my computer, it will be 'activate py3'

5. When generating programme for Santa Fe Trail, input: python ponyge.py --fitness_function santa_fe_trail --grammar_file santa_fe_trail.pybnf --generations 23 --population_size 500 --max_wraps 5

   in this command, fitness_function is the fitness file under fitness, and grammar_file is the grammar file under grammar, ending with .bnf. max_wraps is the number of wraps allowed, if no wrap is permitted in the experiment, remove --max_wraps and the [int] after.

6. Parametre setting is the same for 2048, but the fitness file and grammar file need to be changed to game2048.py and game2048.bnf: python ponyge.py --fitness_function game2048 --grammar_file game2048.pybnf --generations 100 --population_size 500 --max_wraps 3.

7. If the system is not working in your computer, please tell me and I'll bring my computer to your place.
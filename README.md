# facebookChatSImulator
A small python script that analyzes a Facebook chat and simulates sentences from the participants

To use:

Download your facebook chat either through a third party service or by using Facebook's provided archive tool

Run main.py with python3, a usage instruction is provided

(i.e. python3 main.py file_name.html)

Uses simple Markov Chain to generate sentence

A sparse matrix was considered instead of an edge list however sparse matrices appear to take longer to construct 
and the dictionary implementation of an edgelist also offers O(1) access time for the elements

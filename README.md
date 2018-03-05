# facebookChatSImulator
A small python script that analyzes a Facebook chat and simulates sentences from the participants

To use:

Download your facebook chat either through a third party service or by using Facebook's provided archive tool

Run main.py with python3, a usage instruction is provided

(i.e. python3 main.py file_name.html)

Uses simple Markov Chain to generate sentence

A sparse matrix was considered instead of an edge list however sparse matrices appear to take longer to construct 
and the dictionary implementation of an edgelist also offers O(1) access time for the elements

Known Bugs:

There is an issue where on occasion the date metadata in the chat will be parsed into the message due to an
inconsitency in how the chat html files are organized

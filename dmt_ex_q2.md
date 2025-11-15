Q:
Prove that the language A from the previous question is not context-free again, but this time
do so by utilizing the Pumping Lemma for Context-Free Languages.
Consider the language A = {w | w ∈ {a, b, c}∗ ∧ F (w, a) = F (w, b) = F (w, c)} where F (w, a)
counts the number of occurences of character a in string w.


R:
Question 7. Scored out of 2 points.
Pumping Lemma
+ 0.5 pts Student answer has correct overall structure and proof technique (assume language is context free, choose
a string, try to pump it, etc.)
+ 1 pt Student selects a proper string that cannot be pumped and attempts to argue that the string cannot be
pumped through cases.
+ 0.5 pts Student proof actually does cover all cases and is correct.
+ 0.5 pts Close but there is at least one minor mistake. You must tell the student what the mistake that you found is.
+ 0 pts Incorrect or no answer (make sure to provide at least one input that fails so the student has feedback to work
from)


S:
Begin by assuming A is a CFL. Now consider the regular language R = {a∗b∗c∗}.
R already meets the first constraint of A, but applying the second constraint
limits R to just axbxcx|x ≥ 0. As proven in class, this string cannot be pumped.
For the case where v and y each only contain one character each, there are three
different letters to be considered so no matter which two characters are selected
of a, b, c, the number of characters of the one not chosen will be less than the
two pumped characters. In the case where at least one of v and y contain two
characters, when pumped, the letters will be out of order thus breaking the a’s
first, then b’s, then c’s constraint.

lettersLower = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
lettersUpper = {'J','W','B','Q','U','D','M','L','A','R','E','Z','N','S','H','O','G','Y','C','X','T','I','P','F','V','K'}
numbers = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
chars = {'_','-','@','!'}
sqlForce = lettersLower.union(lettersUpper).union(numbers).union(chars).union({',','{','}'})

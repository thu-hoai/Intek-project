# Longest Common Subsequence of two Strings

Write a function that takes two strings `s1` and `s2` and returns the longest common subsequence of `s1` and `s2`.

The longest common subsequence is the longest sequence of characters (case sensitive) such that all of them appear in both of the string, possibly with other characters in between.

For instance:

```javascript
> longestStringSubsequence("ABAZDC", "BACBAD");
"ABAD"
> longestStringSubsequence("AGGTAB", "GXTXAYB");
"GTAB"
> longestStringSubsequence("aaaa", "aa");
"aa"
```

You're allowed to ignore characters to get a longest common subsequence, but the order has to be the same.

Don't worry about performance at first. Just come up with the simplest, most naive solution that you can. Also come up with more test cases if you would like, and it's generally helpful to write out your algorithm either as pseudocode or in natural language before you start coding.

```python
%load_ext conjure
```


    <IPython.core.display.Javascript object>


    Conjure extension is loaded.
    For usage help run: %conjure_help



```python
%%conjure

find x,y,
z : int(0..9)
find xyz 
:     int(400..800)
minimising xyz
such that
  xyz = 100 * 
  x + 10 * y + 
  z,
  x + 
  y
  + z = 15,
  y = 2
  * x
```


```json
{"x": 4, "xyz": 483, "y": 8, "z": 3}
```



```python
%conjure_print
```

    
    find x,y,
    z : int(0..9)
    find xyz 
    :     int(400..800)
    minimising xyz
    such that
      xyz = 100 * 
      x + 10 * y + 
      z,
      x + 
      y
      + z = 15,
      y = 2
      * x
    



```python
%conjure_print_pretty
```

    language Essence 1.3
    
    find x: int(0..9)
    find y: int(0..9)
    find z: int(0..9)
    find xyz: int(400..800)
    minimising xyz
    such that
        xyz = 100 * x + 10 * y + z,
        x + y + z = 15,
        y = 2 * x
    
    



```python
%conjure_print_ast
```


```json
{"mInfo": {"finds": [], "givens": [], "enumGivens": [], "enumLettings": [], "lettings": [], "unnameds": [], "strategyQ": {"Auto": {"Interactive": []}}, "strategyA": {"Auto": {"Interactive": []}}, "trailCompact": [], "trailVerbose": [], "trailRewrites": [], "nameGenState": [], "nbExtraGivens": 0, "representations": [], "representationsTree": [], "originalDomains": [], "trailGeneralised": []}, "mLanguage": {"language": {"Name": "Essence"}, "version": [1, 3]}, "mStatements": [{"Declaration": {"FindOrGiven": ["Find", {"Name": "x"}, {"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 0]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 9]}}]}]]}]}}, {"Declaration": {"FindOrGiven": ["Find", {"Name": "y"}, {"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 0]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 9]}}]}]]}]}}, {"Declaration": {"FindOrGiven": ["Find", {"Name": "z"}, {"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 0]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 9]}}]}]]}]}}, {"Declaration": {"FindOrGiven": ["Find", {"Name": "xyz"}, {"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 400]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 800]}}]}]]}]}}, {"Objective": ["Minimising", {"Reference": [{"Name": "xyz"}, null]}]}, {"SuchThat": [{"Op": {"MkOpEq": [{"Reference": [{"Name": "xyz"}, null]}, {"Op": {"MkOpSum": {"AbstractLiteral": {"AbsLitMatrix": [{"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 1]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 2]}}]}]]}, [{"Op": {"MkOpSum": {"AbstractLiteral": {"AbsLitMatrix": [{"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 1]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 2]}}]}]]}, [{"Op": {"MkOpProduct": {"AbstractLiteral": {"AbsLitMatrix": [{"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 1]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 2]}}]}]]}, [{"Constant": {"ConstantInt": [{"TagInt": []}, 100]}}, {"Reference": [{"Name": "x"}, null]}]]}}}}, {"Op": {"MkOpProduct": {"AbstractLiteral": {"AbsLitMatrix": [{"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 1]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 2]}}]}]]}, [{"Constant": {"ConstantInt": [{"TagInt": []}, 10]}}, {"Reference": [{"Name": "y"}, null]}]]}}}}]]}}}}, {"Reference": [{"Name": "z"}, null]}]]}}}}]}}, {"Op": {"MkOpEq": [{"Op": {"MkOpSum": {"AbstractLiteral": {"AbsLitMatrix": [{"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 1]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 2]}}]}]]}, [{"Op": {"MkOpSum": {"AbstractLiteral": {"AbsLitMatrix": [{"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 1]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 2]}}]}]]}, [{"Reference": [{"Name": "x"}, null]}, {"Reference": [{"Name": "y"}, null]}]]}}}}, {"Reference": [{"Name": "z"}, null]}]]}}}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 15]}}]}}, {"Op": {"MkOpEq": [{"Reference": [{"Name": "y"}, null]}, {"Op": {"MkOpProduct": {"AbstractLiteral": {"AbsLitMatrix": [{"DomainInt": [{"TagInt": []}, [{"RangeBounded": [{"Constant": {"ConstantInt": [{"TagInt": []}, 1]}}, {"Constant": {"ConstantInt": [{"TagInt": []}, 2]}}]}]]}, [{"Constant": {"ConstantInt": [{"TagInt": []}, 2]}}, {"Reference": [{"Name": "x"}, null]}]]}}}}]}}]}]}
```


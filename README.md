<a href="https://github.com/AlrikRr/OSCPBuff/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/issues/AlrikRr/OSCPBuff"></a>
<a href="https://github.com/AlrikRr/OSCPBuff/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/issues/AlrikRr/OSCPBuff"></a>
<a href="https://github.com/AlrikRr/OSCPBuff/network"><img alt="GitHub forks" src="https://img.shields.io/github/issues/AlrikRr/OSCPBuff"></a>
<a href="https://github.com/AlrikRr/OSCPBuff/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/AlrikRr/OSCPBuff"></a>

# OSCPBuff
OSCP Buffer Overflow Tool Box

A simple OSCP Buffer Tool Box that can allow you to :
- Fuzzing a remote app 
- Create a Pattern
- Create Bytearray without badchars
- Exploit or create exploit python script fully fontionnal

# Requirements
Python 3.9 and default libraries  

# Usage

Display available modules :  
```bash
python3 OSCPBuff.py -h
```

Display module help :  
```bash
python3 OSCPBuff.py [module] -h
```

# Modules

## mona

Mona module is a cheatsheet about the mona commands that are very useful during the OSCP Buffer Overflow.  

```bash
python3 OSCPBuff.py mona
```
![mona.gif](/assets/mona.gif)  

## pattern

Pattern module allows you to create a pattern by specifying the size or the output file.  
By default, the output is **pattern.txt** even if you don't precise it.  

```bash
python3 OSCPBuff.py pattern -h
```

`-s` : Set the size of the pattern, must be **int**.  
`-o` : Set the namee of the ouput file.

![pattern.gif](/assets/pattern.gif)  

## badchar

Badchar module create a bytearray and you can exclude some badchar.  

```bash
python3 OSCPBuff.py badchar -h
```

Juste add the badchar you want to exclude from the bytarray :  
```bash
python3 OSCPBuff.py badcar "\x05\x02"
```

![badchar.gif](/assets/badchar.gif)  



## exploit 

**WARNING** The exploit module doen't work by itself but the exploit.py generated works !

The exploit module is pretty heavy, there are a lot of options.  
Options required are :  
- `-i` : Set the IP of the target
- `-p` : Set the PORT of the target 
- `-x` : Set the PREFFIX , like OVERFLOW1 , OVERFLOW2, etc ... 

One of these 2 options are required but not at the same time :
- `-j` : Set the Pattern.txt Junk that you generated with pattern module
- `-y` : Set the Payload.txt that you created using msfvenom

Optional options :  
- `-s` : Set the offset of the buffer
- `-r` : Set the retn value, JMP ESP or control the EIP 
- `-d` : Set the padding, the  number of \x90 NOP

You can chose to generate a python script named *exploit.py* and run this script/edit it as you want. To do so, use the option :
- `--generate` : Generate exploit.py and don't execute the exploit

**Exploit using generate option** :  

![exploit-generate.gif](/assets/exploit-generate.gif)  


If you want to execute the exploit, just don't put the `--generate` option.

**Exploit using pattern.txt** :  

![exploit-pattern.gif](/assets/exploit-pattern.gif)

**Exploit using payload.txt** :  
**NOT WORKING**  

# Contributors

You can contribute as well !  

<a href="https://github.com/AlrikRr/OSCPBuff/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AlrikRr/OSCPBuff" />
</a>

Made with [contributors-img](https://contrib.rocks).


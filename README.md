# Outline-Controller
## control outline vpn using python and crontab to check time validation of every keys and check out user usage with specific limitation
### problems:
when i use outline vpn sloution for my users i see some bugs in this service wich dont let me manage my users correctly:
  1- i see sometime my users use out of them limitation and i have some users with larg mount of trafics so i can not reset them trafics and i must add the last usage of users this couse complexity for me and i lost the real usage of them for every month 
  2- some users are traficless they can not use all them limitation so becouse of that they use them keys more than one month and thats make for me trouble becouse i have a limitation from my isp for  trafic and time
  4- there is no expire function in it so my last users key are valid every mount and i can not find out wich keys are curently using and wich not 
  3- i need alert me to tell me some users key have trouble or expire or limited 
this soulution control time and trafic  of users keys 
its have four part:
 ## 1- status file 
 ```bash
MakeStatus <file name>
 ```
 ## 2- python for call telegram bot for allerting
 
 ## 3- python for call outline api
  
 ## 4- make crontab 
  

 


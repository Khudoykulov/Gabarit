#include <NewPing.h>

#define PIN_TRIG_h 8
#define PIN_ECHO_h 9
#define PIN_TRIG_x 11
#define PIN_ECHO_x 10
#define PIN_TRIG_y 6
#define PIN_ECHO_y 7

#define MAX_DISTANCE 400 

// va maksimal masofani aniqlash uchun doimiydir.
int const_h=29;
int const_x=16;
double const_l=33;

// minimal masofani aniqlash uchun doimiydir.
int min_h=const_h;
int min_x=const_x;
int min_y=const_x;

int d_h=2;
int d_x=2;
int d_y=2;

// vaqtni aniqlash uchun doimiydir.
long Time1=0;
long Time2=0;
long Time3=0;
long Time=0;
// maximal vaqt
long const_time=3000; 

int del;
int flag = 0;
int flag_1 = 0;
int flag_2 = 0;
double vt=0;
double tv=0;
NewPing sonar_h(PIN_TRIG_h, PIN_ECHO_h, MAX_DISTANCE);
NewPing sonar_x(PIN_TRIG_x, PIN_ECHO_x, MAX_DISTANCE);
NewPing sonar_y(PIN_TRIG_y, PIN_ECHO_y, MAX_DISTANCE);

void setup() {
  // Инициализируем взаимодействие по последовательному порту на скорости 9600
  Serial.begin(9600);
}

void loop() {

  // Стартовая задержка, необходимая для корректной работы.
  delay(40);
  Time=millis();
  // Получаем значение от датчика расстояния и сохраняем его в переменную
  unsigned int distance_h = sonar_h.ping_cm();

  unsigned int distance_x = sonar_x.ping_cm();

  unsigned int distance_y = sonar_y.ping_cm();

  // Печатаем расстояние в мониторе порта
del=abs(const_h-distance_h); 
if (del>d_h) {
    
  if (distance_h< min_h) { min_h=distance_h;  
  if (flag==0) {Time1 = millis();  flag=1;}  //kirish vaqt
 // Serial.print(" min_h1= ");
 // Serial.println(min_h);
  
  } 
}   
if (del<d_h && flag==1 && flag_2==0) { flag_2 = 1; Time3= millis();}  //chiqish vaqt  
del=abs(const_x-distance_x); 
  if (del>d_x) {
  if (distance_x< min_x) { min_x=distance_x;  
  if (flag_1==0) {flag_1 = 1;  Time2 = millis();   }
  }  
    }
del=abs(const_x-distance_y); 
    
 if (del>d_y) {
  if (distance_y< min_y) { min_y=distance_y;  
  if (flag_1==0) {flag_1 = 1; Time2 = millis();   }
  }    
    }
//avt tamom chiqishi     
if (flag==1 && flag_1==1) {
if (del<=d_y) {
int h=abs(const_h-min_h);
int w=abs(const_x-min_x-min_y);
tv=abs(Time2-Time1);
//Serial.print(tv);

if (tv>0) { vt=const_l*10/tv;  }  


double t=abs(Time3-Time1);
double lt=vt*t/1000;
int l=floor(lt*100);
    vt=vt*3.6;
  Serial.print("#");
  Serial.print(h);
  Serial.print("#");
  Serial.print(w);
  Serial.print("#");
  Serial.print(l);
  Serial.print("#");
  Serial.print(vt,2);

  Serial.println("#");
  flag=0; flag_1=0; flag_2 = 0;
  min_h=const_h;
  min_x=const_x;
  min_y=const_x;
  Time1=0;
  Time2=0;
  Time3=0;
  } 
  }  
/*   
 if (flag==1 && flag_1==0 && Time-Time3>const_time ) {
  flag=0; flag_1=0;
  min_h=const_h;
  min_x=const_x;
  min_y=const_x;
  Time1=0;
  Time2=0;
  Time3=0;
  
  }
  */
  /*

    
  /Serial.print(" h= ");
  Serial.print(distance_h);
  Serial.print(" x= ");
  Serial.print(distance_x);
  Serial.print(" y= ");
  Serial.print(distance_y);
  Time1 = millis(); 
  Serial.print(" Time1= ");
  Serial.print(Time1);
  
  Serial.println("см");
*/
}

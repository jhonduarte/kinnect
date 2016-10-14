Actualizar/Instalar Xcode a la última versión
Una vez hecho pasa a Xcode / Open Developer Tool / More Developer Tools… e instala Command Line Tools
Instalar CMake

Instalación de dependencias:

En primer lugar, tendremos que downlaod algunas bibliotecas con el fin de conseguir el puerto USB de tu Mac a trabajar con el Kinect junto con el conductor SensorKinect.
Abre tu terminal (Aplicaciones -> Utilidades -> Terminal) y escriba lo siguiente:

- sudo port install libtool
- sudo port install libusb-devel +universal

Una vez finalizado, reinicia tu equipo

# Métodos Computacionales Avanzados - Tarea 3
## Integrantes
- Jimena González 
- Carlos Miguel Patiño 
- Sebastián Caldas Rivera

## Implementación 
La implementación presentada del colapso gravitaciones se basa en la 
aproximación esférica sugerida en clase. La fuerza gravitacional
sobre una estrella m se aproxima entonces a aquella que ejercería una 
partícula con masa M en el centro de la esfera, donde M es la suma de las
masas de aquellas estrellas más cercanas al centro que m. 

El paso crítico en la implementación es entonces encontrar tal masa M
para cada estrella de la simulación. Esta tarea es trivial si se tienen 
las partículas ordenadas por radio, pero el ordenamiento en sí puede 
llegar a ser costoso. Para optimizar el tiempo de ejecución, se plantea 
entonces la siguiente propuesta (que es en sí una nueva aproximación):

1.  Se divide el espacio (10 veces el radio de la esfera inicial) en 
	cascarones esféricos de grosor constante. 
2.  Para cada estrella m se conoce el cascaron en el que se ubica (pues
	se conoce el radio en el que se ubica m y el grosor de los cascarones). 
	Si una estrella cae fuera del espacio considerado (por razones que se
	mencionarán más adelante), se les asigna el cascaron más lejano al centro
	(las coordenadas de la estrella no se alteran). 
3.  Para cada cascaron se conoce la masa de las estrellas allí ubicadas.
4.  La masa M que actuaría sobre m es la suma de las masas de todos los 
	cascarones más cercanos al centro. 

Es notorio entonces que el grosor de los cascarones es un nuevo parámetro 
para la implementación. En este caso en particular, se recibe es el número 
de cascarones en los que se debe dividir la esfera inicial. 

También se debe aclarar que el epsilon de la [implementación de Jaime Forero](https://github.com/forero/SimpleNbody) 
representa aquí la mínima distancia al centro desde la cual una partícula acelera gracias
a interacciones gravitacionales (note que lo mismo sucede dentro del cascaron más 
cercano al centro, por lo que la mínima distancia es entonces la mayor entre el 
grosor de los cascarones y el epsilon).

El comportamiento de la energía para esta aproximación en función del número
de iteraciones es el siguiente:

![Energia](https://github.com/scaldas/MCA_Tarea3/blob/master/img/analisis_energia/energy.png)

donde se utilizaron 1000 estrellas con un epsilon de 0.1 y 600 cascarones (o buckets).

Mientras tanto, el comportamiento de la energía final en función del número de
cascarones es el siguiente:

![Buckets](https://github.com/scaldas/MCA_Tarea3/blob/master/img/analisis_buckets/buckets.png)

donde se utilizaron 1000 estrellas y un epsilon de 0.1 en todas las iteraciones. 

Se observa entonces que, para muy pocos buckets (un número menor a apróximadamente 30% de
las estrellas), el sistema no se comporta correctamente, llegando a tener estados no ligados
con energía positiva. Sabiendo que para estos parámetros la energía inicial es de unos -500, 
se puede inferir que el número de buckets que mejor conserva la energía es uno que se 
encuentre entre 50% y 60% del número de estrellas. Sin embargo, análisis con más 
partículas serían pertinentes (si se tuviera el tiempo para realizarlos). 

## Referencias 
[Referencia 1](http://www.scholarpedia.org/article/N-body_simulations_%28gravitational%29)
[Referencia 2](https://github.com/forero/SimpleNbody)

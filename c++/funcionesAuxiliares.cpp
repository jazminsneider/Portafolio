#include "include/json.hpp"
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <vector>
#include <chrono>

using namespace std;
// Para libreria de JSON.
using namespace nlohmann;

//función que lee los datos y retorna una tupla con 2 listas (las coordenadas en x y las coordenadas en y de cada punto)
tuple<vector<float>, vector<float>> leer_datos(string &datos) {
  string filename = "../../data/" + datos;

  ifstream input(filename);

  json instance;
  input >> instance;
  input.close();
  vector<float> puntosEnX = instance["x"];
  vector<float> puntosEny = instance["y"];
  return {puntosEnX, puntosEny};
}


tuple<vector<float>, vector<float>>
armar_grilla(vector<float> listax, vector<float> listay, int m1, int m2) {
  vector<float> grilla_x;
  float delta1 = (listax.back() - listax.front()) / (m1 - 1); //calculamos la distancia que van a tener todos los puntos de la grilla_x
  float x = listax.front(); //tengo que ir desde el primero hasta el último
  for (int i = 0; i < m1; ++i) {
    grilla_x.push_back(x);
    x += delta1;
  } //vamos añadiendo la cantidad de puntos querida, encontrando los valores de la grilla con el delta

  vector<float> grilla_y = {}; 
  //para grilla y no alcanza con ir desde el primero hasta el ultimo porque no necesariamente las alturas están ordenadas
  float minimo = *min_element(listay.begin(), listay.end()); 
  float maximo = *max_element(listay.begin(), listay.end()); //buscamos el minimo y el maximo elemento
  float delta2 = (maximo - minimo) / (m2 - 1);
  float y = minimo;
  for (int i = 0; i < m2; ++i) {
    grilla_y.push_back(y);
    y += delta2;
  }

  return {grilla_x, grilla_y}; //devolvemos una tupla de listas
}

//Función que calcula el error entre dos puntos
float error(tuple<float, float> BP_inicial, tuple<float, float> BP_final,
            tuple<std::vector<float>, vector<float>> puntos) {
  float suma_de_errores = 0;
  //Recuperamos las coordenadas en x y en y de los breakpoints para calcular la función lineal que une a los puntos
  float x1 = get<0>(BP_inicial);
  float y1 = get<1>(BP_inicial);
  float x2 = get<0>(BP_final);
  float y2 = get<1>(BP_final);
  float pendiente = (y2 - y1) / (x2 - x1);
  float ordenada = y2 - pendiente * x2;
  int i = 0;
   //Buscamos aquellos puntos que se encuentran entre los breakpoints
  while (i < get<0>(puntos).size() && get<0>(puntos)[i] <= x2) {
    //Si el punto se encuentra dentro del rango de los breakpoint entonces calcula su error
    if (x1 < get<0>(puntos)[i]) {
      float yfuncion = pendiente * get<0>(puntos)[i] + ordenada;
      suma_de_errores += abs(get<1>(puntos)[i] - yfuncion);
    }
    i++;
  }
  return suma_de_errores;
}

//calcula el error de una solucion con varios puntos
float errorSolucion(vector<tuple<float, float>> solucion,
                    tuple<vector<float>, vector<float>> puntos) {
  int i = 0;
  float inf = 10e10;
  float errorTotal = 0;
  //Si la solucion no tiene breakpoints, el error total es inf
  if (solucion.size() == 0) {
    errorTotal = inf;
  } 
   //si la solucion tiene solo un punto, el error es el valor absoluto entre el punto calculado por la solucion y el punto pasado por parámetro.
  else if (solucion.size() == 1) {
    errorTotal += abs(get<1>(puntos)[0] - get<1>(solucion[0]));
  } 
  
  else {
    errorTotal+=abs(get<1>(puntos)[0] - get<1>(solucion[0])); //calcula el error del primer punto
    while (i < solucion.size() - 1) { //calcula el error de a pares
      errorTotal += error(solucion[i], solucion[i + 1], puntos);
      i++;
    }
  }
  return errorTotal;
}

// esta funcion es para poder controlar las x que se añadieron a nuestros vectores solucion en la recursion
vector<int> lista_X(vector<tuple<float, float>> coordenadas) {
  vector<int> res = {};
  int i = 0;
  while (i < coordenadas.size()) {
    res.push_back(get<0>(coordenadas[i]));
    i++;
  }
  return res;
}

//esta función reemplaza a la función predefinida "in" en python
bool esta(float punto, vector<tuple<float, float>> sol) {
  bool res = false;
  int i = 0;
  while (i < sol.size()) {
    if (punto == get<0>(sol[i])) {
      res = true;
    }
    i++;
  }

  return res;
}





#include "funcionesAuxiliares.cpp"

tuple<float, vector<tuple<float, float>>, int>
minimoPD(map<tuple<int, int, int>, tuple<float, vector<tuple<float, float>>>>
             superdict,
         int x, int largo_y, int k) {
  float min = 10e10;
  int y_ultima = 0;
  for (int y = 0; y < largo_y; y++) {
    if (get<0>(superdict[make_tuple(x, y, k)]) < min) {
      min = get<0>(superdict[make_tuple(x, y, k)]);
      y_ultima = y;
    }
  }
    return make_tuple(min, get<1>(superdict[make_tuple(x, y_ultima, k)]),
                      y_ultima);
}

  tuple<float, vector<tuple<float, float>>> breakpointsAuxPD(
      int breakpoints, vector<float> grillax, vector<float> grillay,
      map<tuple<int, int, int>, tuple<float, vector<tuple<float, float>>>>
          superdiccionario,
      tuple<vector<float>, vector<float>> npuntos) {
    // Cargamos los errores de los primeros puntos, de esta manera vamos a poder
    // caclcular el minimo de crear una línea entre el breakpoint anterior y el
    // próximo que resulte en el error mínimo. Es para cuando ponemos un 2ndo
    // breakpoint.

    vector<tuple<float, float>> reconstruir_aux = {};

    for (int y = 0; y < grillay.size(); y++) {
      float error_inicial = abs(get<1>(npuntos)[0] - grillay[y]);
      get<0>(superdiccionario[make_tuple(0, y, 0)]) = error_inicial;
    }
    int a = 0;
    int b = 0;
    for (int k = 1; k < breakpoints; k++) {
      for (int x = 1; x < grillax.size(); x++){
          for (int y = 0; y < grillay.size(); y++){
              float min_error = 10e10;
              for (int xi = 0; xi < x; xi++) {
                for (int yi = 0; yi < grillay.size(); yi++){
                    float error_aux =
                        error(make_tuple(grillax[xi], grillay[yi]),
                              make_tuple(grillax[x], grillay[y]), npuntos);
                    float error_total =
                        error_aux +
                        get<0>(superdiccionario[make_tuple(xi, yi, k - 1)]);
                    if (error_total < min_error) {
                      min_error = error_total;
                      a = xi;
                      b = yi;
                      reconstruir_aux = get<1>(superdiccionario[make_tuple(xi, yi, k - 1)]);
                    }
                  }
                    reconstruir_aux.push_back(make_tuple(a, b));
                    superdiccionario[make_tuple(x, y, k)] = make_tuple(min_error, reconstruir_aux);
                    reconstruir_aux.pop_back();
              }
            }
        }
    }
    tuple<float, vector<tuple<float, float>>, int> posiciones_solucion = minimoPD(superdiccionario, grillax.size() - 1, grillay.size(), breakpoints - 1);
    vector<tuple<float, float>> solucion = {}; 
    for(int i=0; i<get<1>(posiciones_solucion).size(); i++){
        solucion.push_back(make_tuple(grillax[get<0>(get<1> (posiciones_solucion)[i])], grillay[get<1>(get<1>(posiciones_solucion)[i])]));
    }
    solucion.push_back(make_tuple(grillax[grillax.size() - 1], grillay[get<2>(posiciones_solucion)]));
    return make_tuple(get<0>(posiciones_solucion), solucion);
  }

  map<tuple<int, int, int>, tuple<float, vector<tuple<float, float>>>>
  inicializar(int breakpoints, int m1, int m2) {
    map<tuple<int, int, int>, tuple<float, vector<tuple<float, float>>>>
        superdiccionario = {};
    float inf = 10e10;
    for (int k = 0; k < breakpoints; k++) {
      for (int i = 0; i < m1; i++) {
        for (int j = 0; j < m2; j++) {
          superdiccionario[make_tuple(i, j, k)] = {inf, {}};
        }
      }
    }
    return superdiccionario;
  }

  tuple<float, vector<tuple<float, float>>> breakpointsPD(
      string archivo, int breakpoints, int m1, int m2) {
    vector<float> puntosEnX = get<0>(leer_datos(archivo));
    vector<float> puntosEnY = get<1>(leer_datos(archivo));
    vector<float> grilla_x = get<0>(armar_grilla(puntosEnX, puntosEnY, m1, m2));
    vector<float> grilla_y = get<1>(armar_grilla(puntosEnX, puntosEnY, m1, m2));
    map<tuple<int, int, int>, tuple<float, vector<tuple<float, float>>>>
        superdiccionario = inicializar(breakpoints, m1, m2);
    return breakpointsAuxPD(breakpoints, grilla_x, grilla_y, superdiccionario,
                 make_tuple(puntosEnX, puntosEnY));
  }

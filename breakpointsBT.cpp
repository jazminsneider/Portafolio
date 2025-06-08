#include "funcionesAuxiliares.cpp"

tuple<float, vector<tuple<float, float>>>
breakpointsAuxBT(int breakpoints, float x, float y, vector<float> grilla_x,
                    vector<float> grilla_y,
                    tuple<vector<float>, vector<float>> npuntos,
                    vector<tuple<float, float>> posible,
                    vector<tuple<float, float>> sol, float error_sol) {

  // aca usamos iteradores ya que no podemos usar la funcion in de python. Si el
  // iterador llego al final implica que el elemento no está en la lista
  if (posible.size() == 1 && !(esta(grilla_x[0], posible))) {
    return make_tuple(error_sol, sol);
  } else if (posible.size() >= 2 and
             errorSolucion(posible, npuntos) >= error_sol) {
    return make_tuple(error_sol, sol);
  } else if (breakpoints > grilla_x.size() - x) {
    return make_tuple(error_sol, sol);
  } else if (breakpoints == 0 && x == grilla_x.size()) {
    float error_posible = errorSolucion(posible, npuntos);
    if (error_posible < error_sol) {
      sol = posible;
      error_sol = error_posible;
    }
    return make_tuple(error_sol, sol);
  }

  else if (x < grilla_x.size() && esta(grilla_x[x], posible)) {
    return make_tuple(error_sol, sol);
  } else if (breakpoints == 0 && x != grilla_x.size()) {
    return make_tuple(error_sol, sol);
  } else if (breakpoints != 0 && x == grilla_x.size()) {
    return make_tuple(error_sol, sol);
  }
  tuple<float, vector<tuple<float, float>>> res = {};
  for (int j = 0; j <= grilla_y.size(); j++) {
    if (j == grilla_y.size()) {
      res = breakpointsAuxBT(breakpoints, x + 1, j, grilla_x, grilla_y,
                                npuntos, posible, sol, error_sol);
      error_sol = get<0>(res);
      sol = get<1>(res);
    } else {
      posible.push_back(make_tuple(grilla_x[x], grilla_y[j]));
      res = breakpointsAuxBT(breakpoints - 1, x + 1, j, grilla_x, grilla_y,
                                npuntos, posible, sol, error_sol);
      error_sol = get<0>(res);
      sol = get<1>(res);
      posible.pop_back();
    }
  }
  return make_tuple(error_sol, sol);
}

tuple<float, vector<tuple<float, float>>>
breakpointsBT(string archivo, int breakpoints, int m1, int m2) {
  vector<float> puntosEnX = get<0>(leer_datos(archivo));
  vector<float> puntosEnY = get<1>(leer_datos(archivo));
  vector<float> grilla_x = get<0>(armar_grilla(puntosEnX, puntosEnY, m1, m2));
  vector<float> grilla_y = get<1>(armar_grilla(puntosEnX, puntosEnY, m1, m2));
  tuple<vector<float>, vector<float>> mis_puntos = {puntosEnX, puntosEnY};

  return breakpointsAuxBT(breakpoints, 0, 0, grilla_x, grilla_y, mis_puntos,
                             {}, {}, 1e10);
}

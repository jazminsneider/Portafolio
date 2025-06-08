#include "funcionesAuxiliares.cpp"

tuple<float, vector<tuple<float, float>>>
breakpointsAuxFB(int breakpoints, float x, float y, vector<float> grilla_x,
                    vector<float> grilla_y,
                    tuple<vector<float>, vector<float>> npuntos,
                    vector<tuple<float, float>> posible,
                    vector<tuple<float, float>> sol, float error_sol) {

  if (breakpoints == 0 && x == grilla_x.size() &&
      !(esta(grilla_x[0], posible))) {

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
      res = breakpointsAuxFB(breakpoints, x + 1, j, grilla_x, grilla_y,
                                npuntos, posible, sol, error_sol);
      error_sol = get<0>(res);
      sol = get<1>(res);
    } else {
      posible.push_back(make_tuple(grilla_x[x], grilla_y[j]));
      res = breakpointsAuxFB(breakpoints - 1, x + 1, j, grilla_x, grilla_y,
                                npuntos, posible, sol, error_sol);
      error_sol = get<0>(res);
      sol = get<1>(res);
      posible.pop_back();
    }
  }
  return make_tuple(error_sol, sol);
  ;
}

tuple<float, vector<tuple<float, float>>>
breakpointsFB(string archivo, int breakpoints, int m1, int m2) {
  vector<float> puntosEnX = get<0>(leer_datos(archivo));
  vector<float> puntosEnY = get<1>(leer_datos(archivo));
  vector<float> grilla_x = get<0>(armar_grilla(puntosEnX, puntosEnY, m1, m2));
  vector<float> grilla_y = get<1>(armar_grilla(puntosEnX, puntosEnY, m1, m2));
  tuple<vector<float>, vector<float>> mis_puntos = {puntosEnX, puntosEnY};

  return breakpointsAuxFB(breakpoints, 0, 0, grilla_x, grilla_y, mis_puntos,
                             {}, {}, 1e10);
}



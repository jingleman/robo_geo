
/*
Python extension of visiLibity Visibility_Polygon wrapper.
See (../../)compile_and_run.

TO DO:
--Tabs --> spaces.
--Eliminate warnings here.
--Modify visiLibity to eliminate warnings there.
*/

#include "visilibity.hpp"		// requires sym link.
#include <numpy/arrayobject.h>  // PyArray, import_array, etc.
#include <Python.h>
#include <stdio.h>
#include <vector>
#include <iostream>
#include <assert.h>
#include <ctime>	// clock
#include <string>

using namespace std;

PyObject *wrap_compute_visibility(PyObject *self, PyObject *args) 
{
	vector<pair<string, clock_t>> clocks;
	clocks.push_back(pair<string, clock_t>(" pre", clock()));

    PyObject *shapes = NULL;
    PyObject *query  = NULL;
    assert(PyArg_ParseTuple(args, "OO", &shapes, &query));
    
    //size_t nCout = 0;
    //cout << " nCout++= " << nCout++ << endl;

    vector<VisiLibity::Polygon> polygons;

    int nShapes = PyList_Size(shapes);
    for(int i = 0; i < nShapes; ++i) {

		PyObject *shape = PyList_GetItem(shapes, i);
		assert(PyArray_NDIM(shape)    == 2);
		assert(PyArray_DIMS(shape)[1] == 2);
		npy_intp nVerts = PyArray_DIMS(shape)[0];
		assert(nVerts >= 3);
		double *dshape = (double*) PyArray_GETPTR1(shape, 0);		// TO DO: use GETPTR2??

		vector<VisiLibity::Point> points;
		for (size_t i = 0; i < nVerts; ++i) {
			double x = dshape[2*i  ];
			double y = dshape[2*i+1];

			VisiLibity::Point point(x, y);
			points.push_back(point);
		}
		VisiLibity::Polygon polygon(points);
		polygons.push_back(polygon);
    }

    VisiLibity::Environment environment(polygons);
	assert(PyArray_NDIM(query)    == 1);
	assert(PyArray_DIMS(query)[0] == 2);
	double *dQuery = (double*) PyArray_GETPTR1(query, 0);
    VisiLibity::Point queryPoint(dQuery[0], dQuery[1]);

	clocks.push_back(pair<string, clock_t>("proc", clock()));
    VisiLibity::Visibility_Polygon visibility_Polygon(queryPoint, environment, 0.0000001);
	clocks.push_back(pair<string, clock_t>("post", clock()));

    npy_intp dims[] = {npy_intp(visibility_Polygon.n()), 2};
    import_array();
    PyObject *output = PyArray_SimpleNew(2, dims, NPY_DOUBLE);
    {
		assert(dims[0] >= 3);
		double *dOut = (double*) PyArray_GETPTR1(output, 0);
		for (size_t i = 0; i < dims[0]; ++i) {		// TO DO: fix types throughout.
			double &x = dOut[2*i  ];
			double &y = dOut[2*i+1];
			//cout << " x y = " << x << " " << y << endl;

			x = visibility_Polygon[i].x();
			y = visibility_Polygon[i].y();
		}
	}


	clocks.push_back(pair<string, clock_t>(" end", clock()));

	double sPrev = 0.0;
	for (auto clock : clocks) {
		cout << clock.first << " : ";
		cout << clock.second << " ";
		double s = double (clock.second) / double (CLOCKS_PER_SEC);
		cout << s << " ";
		if (sPrev != 0.0) cout << s - sPrev << " ";
		sPrev = s;
		cout << endl;
	}

	cout << " query= " << dQuery[0] << " " << dQuery[1] << " area= " << visibility_Polygon.area() << endl;

    return output;
}

static PyMethodDef compute_visibility_methods[] = {
    {    "compute_visibility",
     wrap_compute_visibility,
     METH_VARARGS,
     "Compute visibility polygon from list of numpy arrays defining shapes, and numpy array defining query point."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef compute_visibility_definition = {
    PyModuleDef_HEAD_INIT,
    "compute_visibility",
    "A Python module for computing visibility polygons.",
    -1,
    compute_visibility_methods};

PyMODINIT_FUNC PyInit_compute_visibility(void) {
    Py_Initialize();
    /* https://docs.scipy.org/doc/numpy-1.15.1/user/c-info.how-to-extend.html#required-subroutine */
    //import_array(); # very important!!! ... moved above for now.     
    return PyModule_Create(&compute_visibility_definition);
}

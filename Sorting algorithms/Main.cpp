#include <iostream>
#include <algorithm>
#include <chrono>
#include <random>
#include <iomanip>
#include <cmath>
#include <string>

using namespace std;
using namespace std::chrono;


template <typename T>
void scalaj(T* tablica, int lewy, int srodek, int prawy) {
    int n1 = srodek - lewy + 1;
    int n2 = prawy - srodek;
    T* L = new T[n1];
    T* P = new T[n2];
    for (int i = 0; i < n1; i++) L[i] = tablica[lewy + i];
    for (int j = 0; j < n2; j++) P[j] = tablica[srodek + 1 + j];
    int i = 0, j = 0, k = lewy;
    while (i < n1 && j < n2) {
        if (L[i] <= P[j]) tablica[k++] = L[i++];
        else tablica[k++] = P[j++];
    }
    while (i < n1) tablica[k++] = L[i++];
    while (j < n2) tablica[k++] = P[j++];
    delete[] L; delete[] P;
}

template <typename T>
void m_sort(T* tablica, int lewy, int prawy) {
    if (lewy < prawy) {
        int srodek = lewy + (prawy - lewy) / 2;
        m_sort(tablica, lewy, srodek);
        m_sort(tablica, srodek + 1, prawy);
        scalaj(tablica, lewy, srodek, prawy);
    }
}

template <typename T>
int partycja(T* tablica, int lewy, int prawy) {
    T pivot = tablica[prawy]; 
    int i = lewy - 1;
    for (int j = lewy; j < prawy; j++) {
        if (tablica[j] < pivot) {
            i++;
            swap(tablica[i], tablica[j]);
        }
    }
    swap(tablica[i + 1], tablica[prawy]);
    return i + 1;
}

template <typename T>
void q_sort(T* tablica, int lewy, int prawy) {
    if (lewy < prawy) {
        int pi = partycja(tablica, lewy, prawy);
        q_sort(tablica, lewy, pi - 1);
        q_sort(tablica, pi + 1, prawy);
    }
}

//  INTROSORT I HEAPSORT 

template <typename T>
void napraw_kopiec(T* tablica, int n, int i) {
    int max = i;
    int l = 2 * i + 1, p = 2 * i + 2;
    if (l < n && tablica[l] > tablica[max]) max = l;
    if (p < n && tablica[p] > tablica[max]) max = p;
    if (max != i) {
        swap(tablica[i], tablica[max]);
        napraw_kopiec(tablica, n, max);
    }
}

template <typename T>
void h_sort(T* tablica, int n) {
    for (int i = n / 2 - 1; i >= 0; i--) napraw_kopiec(tablica, n, i);
    for (int i = n - 1; i > 0; i--) {
        swap(tablica[0], tablica[i]);
        napraw_kopiec(tablica, i, 0);
    }
}

template <typename T>
void i_sort_pomoc(T* tablica, int lewy, int prawy, int glebokosc) {
    int n = prawy - lewy + 1;
    if (n < 16) { q_sort(tablica, lewy, prawy); return; }
    if (glebokosc == 0) { h_sort(tablica + lewy, n); return; }
    int pi = partycja(tablica, lewy, prawy);
    i_sort_pomoc(tablica, lewy, pi - 1, glebokosc - 1);
    i_sort_pomoc(tablica, pi + 1, prawy, glebokosc - 1);
}

template <typename T>
void i_sort(T* tablica, int n) {
    i_sort_pomoc(tablica, 0, n - 1, 2 * log2(n));
}

// GENERATORY I TESTY

void gen_losowe(int* t, int n) { for (int i = 0; i < n; i++) t[i] = rand() % 1000000; }
void gen_odwrotne(int* t, int n) { for (int i = 0; i < n; i++) t[i] = n - i; }
void gen_czesciowe(int* t, int n, double p) {
    int lim = (int)(n * p / 100.0);
    for (int i = 0; i < lim; i++) t[i] = i;
    for (int i = lim; i < n; i++) t[i] = rand() % 1000000;
}

void wykonaj_test(int n, string typ, int* base) {
    double s_m = 0, s_q = 0, s_i = 0;
    bool q_failed = false;

    if (typ == "Odwrotne" && n > 10000) {
        q_failed = true;
    }

  
        int* k = new int[n];
        
       
        for(int x=0; x<n-1; x++) k[x] = base[x];
        auto st = high_resolution_clock::now();

        // 2. Quick Sort 
        if (!q_failed) {
            for(int x=0; x<n; x++) k[x] = base[x];
            st = high_resolution_clock::now();
            q_sort(k, 0, n - 1);
            s_q += duration<double, milli>(high_resolution_clock::now() - st).count();
        }
        delete[] k;
  

    cout << n << ";" << typ  << ";";
    if (q_failed) cout << "STACK_OVERFLOW;"; else cout << s_q << ";";
    cout << endl;
}

int main() {
    srand(time(NULL));
    int rozmiary[] = { 100000, 500000, 1000000};
    double procs[] = {25, 50, 75, 99};

    cout << "Rozmiar;Typ;Quick[ms]" << endl;

    for (int n : rozmiary) {
        int* tab = new int[n];

        // Losowe
        gen_losowe(tab, n);
        wykonaj_test(n, "Losowe", tab);

        // Procentowe
        for (double p : procs) {
            gen_czesciowe(tab, n, p);
            wykonaj_test(n, to_string(p) + "%", tab);
        }

        // Odwrotne
        gen_odwrotne(tab, n);
        wykonaj_test(n, "Odwrotne", tab);

        delete[] tab;
    }
    return 0;
}
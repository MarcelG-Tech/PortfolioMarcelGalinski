#ifndef STRUKTURY_HPP
#define STRUKTURY_HPP

#include <stdexcept>

// =====================
// STRUKTURY PODSTAWOWE
// =====================

struct Element {
    int value;
    int priority;
    long long insert_id;
};

struct Node {
    Element data;
    Node* prev;
    Node* next;

    Node(Element d);
};

// =====================
// KOPIEC MAX
// =====================

class KopiecMax {
private:
    Element* tablica;
    int rozmiar;
    int pojemnosc;
    long long global_id;

    bool czyWyzszyPriorytet(const Element& dziecko, const Element& rodzic);
    void heapifyUp(int index);
    void heapifyDown(int index);
    void powiekszTablice();

public:
    KopiecMax(int poczatkowaPojemnosc = 10);
    ~KopiecMax();

    void insert(int wartosc, int priorytet);
    Element extractMax();
    Element peek();
    int returnSize();
    void modifyKey(int wartoscElementu, int nowyPriorytet);
};

// =====================
// LISTA DWUKIERUNKOWA
// =====================

class ListaDwukierunkowa {
private:
    Node* head;
    Node* tail;
    int rozmiar;
    long long global_id;

public:
    ListaDwukierunkowa();
    ~ListaDwukierunkowa();

    void insert(int wartosc, int priorytet);
    Element extractMax();
    Element peek();
    int returnSize();
    void modifyKey(int wartoscElementu, int nowyPriorytet);
};

#endif
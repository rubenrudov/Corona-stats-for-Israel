package com.coronacharts.handlers;

public class GraphPoint {
    private int x, y;

    public GraphPoint(){}

    public GraphPoint(int x, int y){
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public void setX(int x) {
        this.x = x;
    }

    public int getY() {
        return y;
    }

    public void setY(int y) {
        this.y = y;
    }

    @Override
    public String toString() {
        return "GraphPoint{" +
                "x=" + x +
                ", y=" + y +
                '}';
    }
}

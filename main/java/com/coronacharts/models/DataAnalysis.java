package com.coronacharts.models;

import com.google.firebase.database.DataSnapshot;

public class DataAnalysis {
    // TODO: Class for data analytics of country
    private String status, result;

    public DataAnalysis(String status){
        this.status = status;
        if (this.status.equals("אדום")) {
            this.result = "השבים ממדינה זו מחוייבים להכנס לבידוד מרגע הנחיתה בארץ \n נכון לרגע זה, רמת התחלואה במדינה גבוהה והיא מוגדרת כמדינה אדומה";
        } else {
            this.result = "יש להתעדכן באופן שוטף בהנחיות משרד הבריאות \n יש לקחת בחשבון שהמדינה יכולה להפוך לאדומה לפי רמת התחלואה בה בכל עת";
        }
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }
}



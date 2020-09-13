import React from "react";
import "./ClassItem.css";
import {
  IonCard,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonCardContent,
} from "@ionic/react";

export default function ClassItem({ facultyName, subject, date_time }) {
  return (
    <IonCard>
      <IonCardHeader>
        <IonCardSubtitle>{date_time}</IonCardSubtitle>
        <IonCardTitle>{subject}</IonCardTitle>
      </IonCardHeader>

      <IonCardContent>{facultyName}</IonCardContent>
    </IonCard>
  );
}

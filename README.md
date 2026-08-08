# 🌊 AQUADRIVE-AI Core System
> **Autonomous Underwater & Surface Vehicle Control Unit**  
> *نظام هجين ذكي لإدارة الاتصالات والملاحة الذاتية للمركبات المائية*

---

## 👨‍💻 معلومات المهندس والمطور (Developer Profile)

* **الاسم:** حاتم العثامنة (HATEM ATHAMNA)
* **التخصص:** مهندس شبكات واتصالات (Telecommunications & Network Engineer)
* **الهوية والوطن:** ابن فلسطين — مدينة بيت حانون
* **البريد الإلكتروني:** [athamnahatem05@gmail.com](mailto:athamnahatem05@gmail.com)
* **الواتساب للتواصل:** [+213774088297](https://wa.me/213774088297)
* **حساب GitHub:** [hatem686](https://github.com/hatem686)
* **المشروع:** AQUADRIVE-AI Core System

---

## 📐 المعمارية الهندسية ومخطط تدفق البيانات (System Architecture Diagram)

```mermaid
flowchart LR
    A[vision_node] -->|Obstacle Data| C[hybrid_comms_node]
    B[battery_health_monitor] -->|Power Status| C
    E[geofence_guard] -->|GPS Boundary| C
    D[sitl_failover_tester] -.->|Fault Test| C
    C -->|Commands| F[pixhawk_bridge]
    F -->|MAVLink| G[Pixhawk Controller]

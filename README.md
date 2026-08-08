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
graph TD
    subgraph Perception ["Perception Layer - طبقة الإدراك"]
        A["vision_node - AI Vision"]
        B["battery_health_monitor - Power Status"]
    end

    subgraph Safety ["Safety Layer - طبقة الحماية"]
        E["geofence_guard - GPS Boundary"]
    end

    subgraph CoreEngine ["Core Engine - النواة المركزية"]
        C["hybrid_comms_node - Dual Switch"]
        D["sitl_failover_tester - Simulator"]
    end

    subgraph Execution ["Control Layer - طبقة التحكم"]
        F["pixhawk_bridge - MAVLink Interface"]
        G["Pixhawk Flight Controller"]
    end

    A -->|Obstacle Data| C
    B -->|Power Status| C
    E -->|Boundary Guard| C
    D -.->|Fault Testing| C
    C -->|Control Commands| F
    F -->|Pulse Signals| G

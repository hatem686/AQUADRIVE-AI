# 🌊 AQUADRIVE-AI Core System
> **Autonomous Underwater & Surface Vehicle Control Unit**  
> *نظام هجين ذكي لإدارة الاتصالات والملاحة الذاتية للمركبات المائية*

---

## 👨‍💻 معلومات المهندس والمطور (Developer Profile)

* **الاسم:** حاتم العثامنة (HATEM ATHAMNA)
* **التخصص:** مهندس شبكات واتصالات (Telecommunications & Network Engineer)
* **الهوية والوطن:** ابن فلسطين — مدينة بيت حانون
* **البريد الإلكتروني:** [athamnahatem05@gmail.com](mailto:athamnahatem05@gmail.com)
* **الواتساب للتواصل:** [213774088297+](https://wa.me/213774088297)
* **حساب GitHub:** [hatem686](https://github.com/hatem686)
* **المشروع:** AQUADRIVE-AI Core System

---

## 📐 المعمارية الهندسية ومخطط تدفق البيانات (System Architecture Diagram)

```mermaid
graph TD
    %% Custom Styling Definitions
    classDef comms fill:#0284c7,stroke:#38bdf8,stroke-width:3px,color:#fff;
    classDef vision fill:#4f46e5,stroke:#818cf8,stroke-width:2px,color:#fff;
    classDef safety fill:#991b1b,stroke:#f87171,stroke-width:2px,color:#fff;
    classDef hardware fill:#065f46,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef tester fill:#334155,stroke:#94a3b8,stroke-width:2px,color:#fff;

    subgraph Perception ["👁️ طبقة الإدراك والرصد (Perception Layer)"]
        A["📷 vision_node<br/><i>(Computer Vision & AI)</i>"]:::vision
        B["🔋 battery_health_monitor<br/><i>(Power & Range Check)</i>"]:::vision
    end

    subgraph Safety ["🛡️ طبقة الحماية والسلامة (Safety Layer)"]
        E["🗺️ geofence_guard<br/><i>(GPS Geofence Protection)</i>"]:::safety
    end

    subgraph CoreEngine ["🌊 النواة المركزية (Core Engine)"]
        C{"📡 hybrid_comms_node<br/><b>[Dual Communications Switch]</b>"}:::comms
        D["🧪 sitl_failover_tester<br/><i>(Fault Simulation)</i>"]:::tester
    end

    subgraph Execution ["🔗 طبقة التحكم والتحريك (Control & Execution)"]
        F["🔌 pixhawk_bridge<br/><i>(MAVLink Interface)</i>"]:::hardware
        G["🕹️ Pixhawk Flight Controller<br/><i>(Hardware Unit)</i>"]:::hardware
    end

    %% Flow Dynamics
    A -->|1. Obstacle & Path Data| C
    B -->|2. Battery Failover Alert| C
    E -->|3. Boundary Breach Warning| C
    D -.->|Simulated Network Faults| C
    C ==>|4. Safe Navigation Commands| F
    F ==>|5. Actuator Signals| G

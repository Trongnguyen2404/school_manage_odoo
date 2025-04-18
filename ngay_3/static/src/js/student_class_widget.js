/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class StudentClassWidget extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            classList: [],
            selectedClass: "",
            students: [],
            isLoadingClasses: true,
            isLoadingStudents: false,
            error: null,
        });

        onWillStart(async () => {
            await this.loadClasses();
        });
    }

    async loadClasses() {
        this.state.isLoadingClasses = true;
        this.state.error = null;
        try {
            // SỬA LỖI: Truyền mảng rỗng [] thay vì [[]]
            const classes = await this.orm.call(
                "student.record",
                "get_unique_classes_for_owl",
                [] // Không cần truyền tham số bổ sung
            );
            this.state.classList = classes;
             console.log("Classes loaded:", classes);
        } catch (error) {
            console.error("Error loading classes:", error);
            this.state.error = "Không thể tải danh sách lớp.";
        } finally {
            this.state.isLoadingClasses = false;
        }
    }

    async fetchStudents() {
        if (!this.state.selectedClass) {
            this.state.students = [];
            return;
        }
        this.state.isLoadingStudents = true;
        this.state.error = null;
        try {
            const studentsData = await this.orm.call(
                "student.record",
                "get_students_for_owl_widget",
                [this.state.selectedClass] // Truyền tên lớp đã chọn
            );
            this.state.students = studentsData;
            console.log(`Students for class '${this.state.selectedClass}':`, studentsData);
        } catch (error) {
            console.error(`Error fetching students for class ${this.state.selectedClass}:`, error);
            this.state.error = `Không thể tải danh sách sinh viên cho lớp ${this.state.selectedClass}.`;
            this.state.students = [];
        } finally {
            this.state.isLoadingStudents = false;
        }
    }

    onClassChange(ev) {
        this.state.selectedClass = ev.target.value;
        this.fetchStudents();
    }
}

StudentClassWidget.template = "ngay_3.StudentClassWidget";
registry.category("actions").add("ngay_3.student_class_action_tag", StudentClassWidget);
export default StudentClassWidget;
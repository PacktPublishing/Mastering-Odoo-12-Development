odoo.define('school.tour', function(require) {
    "use strict";
    
    var core = require('web.core');
    var tour = require('web_tour.tour');
    
    var _t = core._t;
    
    tour.register('school_tour', {
        url: "/web",
        test: true,
    }, [tour.STEPS.SHOW_APPS_MENU_ITEM, {
        trigger: '.o_app[data-menu-xmlid="school.menu_school_root"]',
        content: _t('Click here to start managing your school.'),
        position: 'bottom',
    }, {
        trigger: 'a[data-menu-xmlid="school.school_group_menu"]',
        content: _t('Click here to start creating groups that will contain students.'),
        position: 'bottom',
    }, {
        trigger: '.o_list_button_add',
        extra_trigger: 'th[data-name="supervisor_id"]',
        content: _t('Click here to create a new group.'),
        position: 'bottom',
        width: 200,
    }, {
        trigger: 'input[name="name"]',
        content: _t("Enter the group's name"),
        position: 'right',
    }, {
        trigger: '.o_form_button_save',
        content: _t('Save this group and the modifications you\'ve made to it.'),
        position: 'bottom',
    }, {
        trigger: 'a[data-menu-xmlid="school.school_student_menu"]',
        content: _t('Click here to manage students.'),
        position: 'bottom',
    }, {
        trigger: 'button[data-view-type="kanban"]',
        content: _t('Click here to easily view and filter students.'),
        position: 'bottom',
        width: 200,
    }, {
        trigger: '.o-kanban-button-new',
        content: _t('Click here to register a new student.'),
        position: 'bottom',
        width: 200,
    }, {
        trigger: 'input[name="name"]',
        content: _t("Enter the student's name"),
        position: 'right',
    },{
        trigger: '.o_field_widget[name="school_group_id"]',
        content: _t('Select the group to which this student belongs.'),
        run: function (actions) {
            actions.text("Test", this.$anchor.find("input"));
        },
        position: 'top',
    }, {
        trigger: ".ui-autocomplete > li > a",
        auto: true,
    }, {
        trigger: '.o_form_button_save',
        content: _t('Save this student and the modifications you\'ve made to it.'),
        position: 'bottom',
    }, {
        trigger: 'a[data-menu-xmlid="school.school_my_students_menu"]',
        content: _t('Quickly access the students assigned to you through this menu.'),
        position: 'bottom',
    }, {
        trigger: "a.o_school_student:contains('Test')",
        content: _t("Click to access a student's information quickly."),
        position: 'right',
    }
]);
    
    });
    
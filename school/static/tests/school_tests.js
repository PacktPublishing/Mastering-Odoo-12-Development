odoo.define('school.tests', function (require) {
    "use strict";
    
    var testUtils = require('web.test_utils');
    var core = require('web.core');
    
    var MyStudents = require('school.my_students');
    
QUnit.module('School', {
    beforeEach: function () {
        this.data = {
            'res.partner': {
                fields: {
                    name: {string: 'Name', type: 'char'},
                    supervisor_id: {string: 'Supervisor ID', type: 'integer'},
                },
                records: [{
                    id: 1,
                    name: "Student A",
                    supervisor_id: 3,
                },
                {
                    id: 2,
                    name: "Student B",
                    supervisor_id: 1,
                },
                {
                    id: 3,
                    name: "Student C",
                    supervisor_id: 3,
                }
                ],
            },
            'ir.ui.view': {
                fields: {
                    name: {string: 'Name', type: 'char'},
                },
                records: [{
                    id: 1,
                    name: "student.form",
                }],
            },
        };
    },
}, function () {
    QUnit.test('Render & Correct user count', async function (assert) {
        assert.expect(2);

        var $target = $('#qunit-fixture');

        var clientAction = new MyStudents(null, {});
        testUtils.addMockEnvironment(clientAction, {
            data: this.data,
            session: {
                uid: 2,
                partner_id: 3,
                name: 'Test User',
            },
        });
        await clientAction.appendTo($target);

        assert.strictEqual(clientAction.$('.o_school_students h1').text(), 'Welcome, Test User',
            "should have rendered the client action without crashing");
        
        assert.strictEqual(clientAction.$('a.o_school_student').length, 2,
            "there should only be 2 students")

        clientAction.destroy();
    });

});
    
    });
    
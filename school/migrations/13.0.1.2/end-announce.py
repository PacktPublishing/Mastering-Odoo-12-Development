from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    global_channel = env.ref("mail.channel_all_employees")
    body = """
        <html>
            The School module has been upgraded to version 1.1 🎉!<br/>
            What's new in this release?<br/>
            <ul>
            <li><tt>student_count</tt> field is now stored</li>
            </ul>
        </html>"""
    global_channel.message_post(body=body, subtype="mail.mt_comment")

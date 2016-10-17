"""empty message

Revision ID: 928ff2746845
Revises: 7a73f487bdca
Create Date: 2016-10-17 12:55:22.186689

"""

# revision identifiers, used by Alembic.
revision = '928ff2746845'
down_revision = '7a73f487bdca'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('confignotificationtemplate')
    op.add_column('confignotificationtype', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('confignotificationtype', sa.Column('email_html_template', sa.String(length=500), nullable=True))
    op.add_column('confignotificationtype', sa.Column('email_template', sa.String(length=500), nullable=True))
    op.add_column('confignotificationtype', sa.Column('sms_template', sa.String(length=160), nullable=True))
    op.add_column('emailmessage', sa.Column('message_subject', sa.String(length=255), nullable=True))
    op.add_column('emailmessage', sa.Column('notification_type_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'emailmessage', 'confignotificationtype', ['notification_type_id'], ['id'])
    op.add_column('smsmessage', sa.Column('notification_type_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'smsmessage', 'confignotificationtype', ['notification_type_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'smsmessage', type_='foreignkey')
    op.drop_column('smsmessage', 'notification_type_id')
    op.drop_constraint(None, 'emailmessage', type_='foreignkey')
    op.drop_column('emailmessage', 'notification_type_id')
    op.drop_column('emailmessage', 'message_subject')
    op.drop_column('confignotificationtype', 'sms_template')
    op.drop_column('confignotificationtype', 'email_template')
    op.drop_column('confignotificationtype', 'email_html_template')
    op.drop_column('confignotificationtype', 'date_created')
    op.create_table('confignotificationtemplate',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('code', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('notification_type_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('email_template', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('sms_template', mysql.VARCHAR(length=160), nullable=True),
    sa.ForeignKeyConstraint(['notification_type_id'], [u'confignotificationtype.id'], name=u'confignotificationtemplate_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###

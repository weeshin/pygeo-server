"""init tables

Revision ID: 0fa25547e977
Revises: 
Create Date: 2024-12-18 00:35:06.852622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fa25547e977'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'layer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('abstract', sa.String(), nullable=True),
        sa.Column('queryable', sa.Boolean(), nullable=True),
        sa.Column('opaque', sa.Boolean(), nullable=True),
        sa.Column('west_bound_longitude', sa.String(), nullable=True),
        sa.Column('east_bound_longitude', sa.String(), nullable=True),
        sa.Column('south_bound_latitude', sa.String(), nullable=True),
        sa.Column('north_bound_latitude', sa.String(), nullable=True),        
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'keywords',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('layer_id', sa.String(), nullable=True),
        sa.Column('keyword', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'crss',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('layer_id', sa.String(), nullable=True),
        sa.Column('crs', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'map_formats',
        sa.Column('id', sa.Integer(), nullable=False),        
        sa.Column('format', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Insert initial data
    conn = op.get_bind()

    # Insert into 'layer' table
    conn.execute(
        sa.text(
            """
            INSERT INTO layer (id, name, title, abstract, queryable, opaque, west_bound_longitude, east_bound_longitude, south_bound_latitude, north_bound_latitude) VALUES
            (1, 'Layer1', 'Layer Title 1', 'This is the first layer', TRUE, FALSE, '100.6238350820671', '102.91331158996276', '2.8201217928695064', '5.558142856024738'),
            (2, 'Layer2', 'Layer Title 2', 'This is the second layer', FALSE, TRUE, '100.6238350820671', '102.91331158996276', '2.8201217928695064', '5.558142856024738');
            """
        )
    )

    # Insert into 'keywords' table
    conn.execute(
        sa.text(
            """
            INSERT INTO keywords (id, layer_id, keyword) VALUES
            (1, 1, 'GIS'),
            (2, 1, 'Mapping'),
            (3, 2, 'Geospatial'),
            (4, 2, 'Raster');
            """
        )
    )

    # Insert into 'crss' table
    conn.execute(
        sa.text(
            """
            INSERT INTO crss (id, layer_id, crs) VALUES
            (1, 1, 'EPSG:4321'),
            (2, 1, 'EPSG:32647'),
            (3, 2, 'EPSG:4321'),
            (4, 2, 'EPSG:32647');
            """
        )
    )

    # Insert into 'map_formats' table
    conn.execute(
        sa.text(
            """
            INSERT INTO map_formats (id, format) VALUES
            (1, 'image/png'),
            (2, 'application/atom+xml'),
            (3, 'application/json;type=geojson'),
            (4, 'application/json;type=topojson'),
            (5, 'application/json;type=utfgrid');            
            """
        )
    )


def downgrade() -> None:
    op.drop_table('layer')
    op.drop_table('keywords')
    op.drop_table('crss')
    op.drop_table("map_formats")

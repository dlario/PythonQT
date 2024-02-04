## Copyright 2023 David Lario
__author__ = 'David Lario'

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

## Revision History
## October 27, 2023 - David James Lario - Created

from sqlalchemy import JSON, Column, DateTime, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from PackageManager.Packages.ProgramBase.Database.dbBase import MainBase


# region Lists
class Country(MainBase):
    __tablename__ = 'lstcountry'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class City(MainBase):
    __tablename__ = 'lstcity'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class Province(MainBase):
    __tablename__ = 'lstprovince'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class PostalCode(MainBase):
    __tablename__ = 'lstpostalcode'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)

class AoGType(MainBase):
    __tablename__ = 'lstaogtype'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class AoGItem(MainBase):
    __tablename__ = 'lstaogitem'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)

class MunicipalityType(MainBase):
    __tablename__ = 'lstmunicipalitytype'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)

class Municipality(MainBase):
    __tablename__ = 'lstmunicipality'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    Name = Column(String(75), unique=True)
    Tags = Column(String(255))
# endregion


# region Tables
class AreaOfGovernance(MainBase):
    __tablename__ = 'areaofgovernance'
    id = Column(Integer, primary_key=True)
    Table_id = Column(Integer)
    Record_id = Column(Integer)
    Parent_id = Column(Integer, ForeignKey('areaofgovernance.id'), nullable=True)
    Children = relationship("AreaOfGovernance", backref='parent', remote_side=[id])
    Tags = Column(String(255))

    def __repr__(self):
        return f"<AreaOfGovernance(name='{self.name}', type='{self.type}')>"


class LocationGeoTag(MainBase):
    __tablename__ = 'locationgeotag'
    id = Column(Integer, primary_key=True)
    locationtype_id = Column(Integer)
    locationitem_id = Column(Integer)
    CenterGeoTagLat = Column(Float(15))
    CenterGeoTagLong = Column(Float(15))
    RadiusGeoTag = Column(Float(15))
    NEGeoTagLat = Column(Float(15))
    NEGeoTagLong = Column(Float(15))
    SWGeoTagLat = Column(Float(15))
    SWGeoTagLong = Column(Float(15))
    What3Words = Column(String(255))


class GeoFence(MainBase):
    __tablename__ = 'geofence'
    id = Column(Integer, primary_key=True)
    Name = Column(String(75))
    Name_id = Column(Integer)
    GeoFenceType = Column(Integer)
    Description = Column(String(255))


class GeoFencePoints(MainBase):
    __tablename__ = 'geofence'
    id = Column(Integer, primary_key=True)
    GeoFenceId = Column(Integer)
    GeoTag = Column(Integer)


class AllLocationGeoTag(MainBase):
    __tablename__ = 'alllocationgeotag'
    id = Column(Integer, primary_key=True)
    locationtype_id = Column(Integer)
    locationitem_id = Column(Integer)
    GeoTag = Column(String(15))
    What3Words = Column(String(255))


class GPSData(MainBase):
    __tablename__ = 'gpsdata'
    id = Column(Integer, primary_key=True)
    Equipment_id = Column(Integer)
    GeoTag = Column(String(75))
    Timestamp = Column(String(75))
    Activity = Column(String(500))
    Velocity = Column(Integer)
    Heading = Column(Integer)
    Altitude = Column(Integer)
    CSTILL = Column(Integer)
    IN_VEHICLE = Column(Integer)
    WALKING = Column(Integer)
    RUNNING = Column(Integer)
    TILTING = Column(Integer)
    UNKNOWN = Column(Integer)
    ON_BICYCLE = Column(Integer)
    IN_RAIL_VEHICLE = Column(Integer)
    IN_ROAD_VEHICLE = Column(Integer)
    EXITING_VEHICLE = Column(Integer)


# endregion
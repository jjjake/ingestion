from server_support import server

from amara.thirdparty import httplib2
from amara.thirdparty import json
from nose.tools import nottest


CT_JSON = {"Content-Type": "application/json"}
HEADERS = {
    "Content-Type": "application/json",
    "Context": "{}",
    }

H = httplib2.Http()


def test_artstor_source_fetching():
    """
    Fetching Artstor document source
    """

    INPUT_JSON = """{
   "_id": "artstor--oai:oaicat.oclc.org:AKRESS_10310356231",
   "_rev": "1-56c6a0d094f7642d53dc0f5fb7dc0c6b",
   "description": "Full view; pre-restoration; Formerly in the Contini Bonacossi Collection, Florence.",
   "rights": [
       "",
       "Please note that if this image is under copyright, you may need to contact one or more copyright owners for any use that is not permitted under the ARTstor Terms and Conditions of Use or not otherwise permitted by law. While ARTstor tries to update contact information, it cannot guarantee that such information is always accurate. Determining whether those permissions are necessary, and obtaining such permissions, is your sole responsibility."
   ],
   "dplaSourceRecord": {
       "handle": [
           "Thumbnail: http://media.artstor.net/imgstor/size2/kress/d0001/kress_1091_post_as.jpg",
           "Image View: http://www.artstor.org/artstor/ViewImages?id=8DtZYyMmJloyLyw7eDt5QHgr&userId=gDBAdA%3D%3D",
           "Ranking: 13000"
       ],
       "description": "Full view; pre-restoration; Formerly in the Contini Bonacossi Collection, Florence.",
       "format": [
           "41.5 x 23.3 cm",
           "Tempera and gold leaf on poplar panel",
           "panel "
       ],
       "rights": [
           "",
           "Please note that if this image is under copyright, you may need to contact one or more copyright owners for any use that is not permitted under the ARTstor Terms and Conditions of Use or not otherwise permitted by law. While ARTstor tries to update contact information, it cannot guarantee that such information is always accurate. Determining whether those permissions are necessary, and obtaining such permissions, is your sole responsibility."
       ],
       "label": "Madonna and Child with Saints",
       "datestamp": "2011-11-07",
       "creator": "Guariento d'Arpo, Italian, c. 1310-1368/70",
       "coverage": [
           "",
           "Repository: North Carolina Museum of Art."
       ],
       "date": "c. 1360",
       "title": "Madonna and Child with Saints",
       "type": [
           "Paintings",
           "Painting"
       ],
       "id": "oai:oaicat.oclc.org:AKRESS_10310356231",
       "subject": "Madonna and Child with Saints; Virgin and Child.; Francis, of Assisi, Saint, 1182-1226.; Giles, Saint, 8th century.; Virgin and Child--with Saint(s).; Jesus Christ.; Mary, Blessed Virgin, Saint.; Anthony, Abbot, Saint, ca. 251-356.; John, the Baptist, Saint."
   },
   "created": {
       "start": "1360-01-01",
       "end": "1360-01-01",
       "displayDate": "c. 1360"
   },
   "ingestDate": "2013-02-02T01:12:27.659532",
   "dplaContributor": {
       "@id": "http://dp.la/api/contributor/artstor",
       "name": "ARTstor OAICatMuseum"
   },
   "TBD_physicalformat": [
       "41.5 x 23.3 cm",
       "Tempera and gold leaf on poplar panel",
       "panel"
   ],
   "creator": "Guariento d'Arpo, Italian, c. 1310-1368/70",
   "title": "Madonna and Child with Saints",
   "source": "Thumbnail: http://media.artstor.net/imgstor/size2/kress/d0001/kress_1091_post_as.jpg",
   "spatial": [
       {
           "name": ""
       },
       {
           "name": "Repository: North Carolina Museum of Art."
       }
   ],
   "isPartOf": {
       "@id": "http://dp.la/api/collections/artstor--SetDPLA",
       "name": "SetDPLA",
       "description": "SetDPLA"
   },
   "@context": {
       "iso639": "dpla:iso639",
       "@vocab": "http://purl.org/dc/terms/",
       "end": {
           "@id": "dpla:end",
           "@type": "xsd:date"
       },
       "name": "xsd:string",
       "dplaSourceRecord": "dpla:sourceRecord",
       "dpla": "http://dp.la/terms/",
       "coordinates": "dpla:coordinates",
       "dplaContributor": "dpla:contributor",
       "start": {
           "@id": "dpla:start",
           "@type": "xsd:date"
       },
       "state": "dpla:state",
       "iso3166-2": "dpla:iso3166-2",
       "LCSH": "http://id.loc.gov/authorities/subjects"
   },
   "ingestType": "item",
   "@id": "http://dp.la/api/items/36a3ac936167a48e2f4ddf5c99f5cf1d",
   "id": "36a3ac936167a48e2f4ddf5c99f5cf1d",
   "subject": [
       {
           "name": "Madonna and Child with Saints"
       },
       {
           "name": "Virgin and Child"
       },
       {
           "name": "Francis, of Assisi, Saint, 1182-1226"
       },
       {
           "name": "Giles, Saint, 8th century"
       },
       {
           "name": "Virgin and Child--with Saint(s)"
       },
       {
           "name": "Jesus Christ"
       },
       {
           "name": "Mary, Blessed Virgin, Saint"
       },
       {
           "name": "Anthony, Abbot, Saint, ca. 251-356"
       },
       {
           "name": "John, the Baptist, Saint"
       }
   ]
}
"""

    EXPECTED_SOURCE = "http://www.artstor.org/artstor/ViewImages?id=8DtZYyMmJloyLyw7eDt5QHgr&userId=gDBAdA%3D%3D"

    url = server() + "artstor_select_isshownat"
    resp,content = H.request(url,"POST",body=INPUT_JSON,headers=CT_JSON)
    assert str(resp.status).startswith("2")

    FETCHED_SOURCE = json.loads(content)[u"source"]
    print FETCHED_SOURCE
    print EXPECTED_SOURCE
    assert FETCHED_SOURCE == EXPECTED_SOURCE
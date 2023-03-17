from utils.db import db
from models.client import Client
from models.Job import Job

def dbQuery(data, fun):
    try:
        db.session()
        result = fun(data)
        db.session.commit()
        return result
    except Exception as e:
        raise Exception(e.message)
    finally:
        db.session.close()

def updateObject(object):
    try:
        db.session()
        db.session.add(object)
        db.session.commit()
    except Exception as e:
        raise Exception(e)
    finally:
        db.session.close()

def findClientByPhoneNumber(phoneNumber):
    client = Client.query.filter_by(phone_number = phoneNumber).one_or_none()
    if client:
        for job in client.jobs: db.session.expunge(job)
        db.session.expunge(client)
    return client

def findClients(phoneNumber):
    if phoneNumber: clients = Client.query.filter_by(phone_number = phoneNumber).all()
    else: clients = Client.query.all()
    for client in clients: db.session.expunge(client)
    return clients

def findJobById(jobId):
    job =Job.query.filter_by(id = jobId).one_or_none()
    if job:
        db.session.expunge(job.customer)
        db.session.expunge(job)
    return job

def findClientById(clientId):
    client = Client.query.filter_by(id = clientId).one_or_none()
    if client: db.session.expunge(client)
    return client
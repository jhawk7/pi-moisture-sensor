from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

import os

'''
pip install opentelemetry-api
pip install opentelemetry-sdk
pip install opentelemetry-exporter-otlp-proto-grpc
'''

class Opentel
  def __init__():
    self.service_name = str(os.getenv("SERVICE_NAME", "default_service"))
    self.exporter_endpoint = str(os.getenv("OPENTEL_EXPORTER_ENDPOINT", "0.0.0.0:4317"))
    self.__initTraceProvider()
    self.__initMeterProvider()

  def __initTraceProvider(self):
    resource = Resource(attributes={
      SERVICE_NAME: self.service_name
    })
    
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=self.exporter_endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

  def __initMeterProvider(self):
    resource = Resource(attributes={
      SERVICE_NAME: self.service_name
    })

    reader = PeriodicExportingMetricReader(
      OTLPMetricExporter(endpoint=self.exporter_endpoint)
    )
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

  def get_tracer(self, name):
    return trace.get_tracer(str(name))

  def get_meter(self, name):
    return metrics.get_meter(str(name))

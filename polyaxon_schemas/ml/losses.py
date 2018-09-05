# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema
from polyaxon_schemas.utils import Tensor


class BaseLossSchema(Schema):
    input_layer = Tensor(allow_none=True)
    output_layer = Tensor(allow_none=True)
    weights = fields.Float(default=1.0, missing=1.0)
    name = fields.Str(allow_none=True)
    collect = fields.Bool(default=True, missing=True)


class BaseLossConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['input_layer', 'output_layer', 'name']

    def __init__(self, input_layer=None, output_layer=None, weights=1.0, name=None, collect=True):
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.weights = weights
        self.name = name
        self.collect = collect


class AbsoluteDifferenceSchema(BaseLossSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return AbsoluteDifferenceConfig(**data)

    @post_dump
    def unmake(self, data):
        return AbsoluteDifferenceConfig.remove_reduced_attrs(data)


class AbsoluteDifferenceConfig(BaseLossConfig):
    """Adds an Absolute Difference loss to the training procedure.

    `weights` acts as a coefficient for the loss. If a scalar is provided, then
    the loss is simply scaled by the given value. If `weights` is a `Tensor` of
    shape `[batch_size]`, then the total loss for each sample of the batch is
    rescaled by the corresponding element in the `weights` vector. If the shape of
    `weights` matches the shape of `predictions`, then the loss of each
    measurable element of `predictions` is scaled by the corresponding value of
    `weights`.

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: AbsoluteDifference
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      loss:
        AbsoluteDifference:
          input_layer: labels
          output_layer: dense_out
      # other model properties
    ```
    """
    IDENTIFIER = 'AbsoluteDifference'
    SCHEMA = AbsoluteDifferenceSchema


class MeanSquaredErrorSchema(BaseLossSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return MeanSquaredErrorConfig(**data)

    @post_dump
    def unmake(self, data):
        return MeanSquaredErrorConfig.remove_reduced_attrs(data)


class MeanSquaredErrorConfig(BaseLossConfig):
    """Computes Mean Square Loss.

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: MeanSquaredError
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      loss:
        MeanSquaredError:
          input_layer: labels
          output_layer: dense_out
      # other model properties
    ```
    """
    IDENTIFIER = 'MeanSquaredError'
    SCHEMA = MeanSquaredErrorSchema


class LogLossSchema(BaseLossSchema):
    epsilon = fields.Float(default=1e-7, missing=1e-7)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return LogLossConfig(**data)

    @post_dump
    def unmake(self, data):
        return LogLossConfig.remove_reduced_attrs(data)


class LogLossConfig(BaseLossConfig):
    """Computes Huber Loss for DQN.

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.
        epsilon: A small value.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: LogLoss
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      loss:
        LogLoss:
          input_layer: labels
          output_layer: dense_out
      # other model properties
    ```
    """
    IDENTIFIER = 'LogLoss'
    SCHEMA = LogLossSchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 epsilon=1e-7,
                 name=None,
                 collect=True):
        super(LogLossConfig, self).__init__(input_layer, output_layer, weights, name, collect)
        self.epsilon = epsilon


class HuberLossSchema(BaseLossSchema):
    clip = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return HuberLossConfig(**data)

    @post_dump
    def unmake(self, data):
        return HuberLossConfig.remove_reduced_attrs(data)


class HuberLossConfig(BaseLossConfig):
    """Computes Huber Loss for DQN.

    [Wikipedia link](https://en.wikipedia.org/wiki/Huber_loss)
    [DeepMind link](https://sites.google.com/a/deepmind.com/dqn/)

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: HuberLoss
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      loss:
        HuberLoss:
          clip: 0.2
      # other model properties
    ```
    """
    IDENTIFIER = 'HuberLoss'
    SCHEMA = HuberLossSchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 clip=0.,
                 name=None,
                 collect=True):
        super(HuberLossConfig, self).__init__(input_layer, output_layer, weights, name, collect)
        self.clip = clip


class ClippedDeltaLossSchema(BaseLossSchema):
    clip_value_min = fields.Float(default=-1., missing=-1.)
    clip_value_max = fields.Float(default=-1., missing=-1.)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ClippedDeltaLossConfig(**data)

    @post_dump
    def unmake(self, data):
        return ClippedDeltaLossConfig.remove_reduced_attrs(data)


class ClippedDeltaLossConfig(BaseLossConfig):
    """Computes clipped delta Loss for DQN.

    [Wikipedia link](https://en.wikipedia.org/wiki/Huber_loss)
    [DeepMind link](https://sites.google.com/a/deepmind.com/dqn/)

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.
        clip_value_min: default to -1.
        clip_value_max: default to 1.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: ClippedDeltaLoss
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      loss:
        ClippedDeltaLoss:
          clip_value_min: -0.8
      # other model properties
    ```
    """
    IDENTIFIER = 'ClippedDeltaLoss'
    SCHEMA = ClippedDeltaLossSchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 clip_value_min=-1.,
                 clip_value_max=1.,
                 name=None,
                 collect=True):
        super(ClippedDeltaLossConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)
        self.clip_value_min = clip_value_min
        self.clip_value_max = clip_value_max


class SoftmaxCrossEntropySchema(BaseLossSchema):
    label_smoothing = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SoftmaxCrossEntropyConfig(**data)

    @post_dump
    def unmake(self, data):
        return SoftmaxCrossEntropyConfig.remove_reduced_attrs(data)


class SoftmaxCrossEntropyConfig(BaseLossConfig):
    """Computes Softmax Cross entropy (softmax categorical cross entropy).

    Computes softmax cross entropy between y_pred (logits) and
    y_true (labels).

    Measures the probability error in discrete classification tasks in which
    the classes are mutually exclusive (each entry is in exactly one class).
    For example, each CIFAR-10 image is labeled with one and only one label:
    an image can be a dog or a truck, but not both.

    **WARNING:** This op expects unscaled logits, since it performs a `softmax`
    on `y_pred` internally for efficiency.  Do not call this op with the
    output of `softmax`, as it will produce incorrect results.

    `y_pred` and `y_true` must have the same shape `[batch_size, num_classes]`
    and the same dtype (either `float32` or `float64`). It is also required
    that `y_true` (labels) are binary arrays (For example, class 2 out of a
    total of 5 different classes, will be define as [0., 1., 0., 0., 0.])

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.
        label_smoothing: If greater than `0` then smooth the labels.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: SoftmaxCrossEntropy
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      loss:
        SoftmaxCrossEntropy:
          label_smoothing: 0.1
      # other model properties
    ```
    """
    IDENTIFIER = 'SoftmaxCrossEntropy'
    SCHEMA = SoftmaxCrossEntropySchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 label_smoothing=0.,
                 name=None,
                 collect=True):
        super(SoftmaxCrossEntropyConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)
        self.label_smoothing = label_smoothing


class SigmoidCrossEntropySchema(BaseLossSchema):
    label_smoothing = fields.Float(default=0., missing=0.)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SigmoidCrossEntropyConfig(**data)

    @post_dump
    def unmake(self, data):
        return SigmoidCrossEntropyConfig.remove_reduced_attrs(data)


class SigmoidCrossEntropyConfig(BaseLossConfig):
    """Computes Sigmoid cross entropy.(binary cross entropy):

    Computes sigmoid cross entropy between y_pred (logits) and y_true
    (labels).

    Measures the probability error in discrete classification tasks in which
    each class is independent and not mutually exclusive. For instance,
    one could perform multilabel classification where a picture can contain
    both an elephant and a dog at the same time.

    For brevity, let `x = logits`, `z = targets`.  The logistic loss is

      x - x * z + log(1 + exp(-x))

    To ensure stability and avoid overflow, the implementation uses

      max(x, 0) - x * z + log(1 + exp(-abs(x)))

    `y_pred` and `y_true` must have the same type and shape.

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.
        label_smoothing: If greater than `0` then smooth the labels.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: SigmoidCrossEntropy
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      loss:
        SigmoidCrossEntropy:
          label_smoothing: 0.1
      # other model properties
    ```
    """
    IDENTIFIER = 'SigmoidCrossEntropy'
    SCHEMA = SigmoidCrossEntropySchema

    def __init__(self,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 label_smoothing=0.,
                 name=None,
                 collect=True):
        super(SigmoidCrossEntropyConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)
        self.label_smoothing = label_smoothing


class HingeLossSchema(BaseLossSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return HingeLossConfig(**data)

    @post_dump
    def unmake(self, data):
        return HingeLossConfig.remove_reduced_attrs(data)


class HingeLossConfig(BaseLossConfig):
    """Hinge Loss.

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: HingeLoss
      # other model properties
    ```
    """
    IDENTIFIER = 'HingeLoss'
    SCHEMA = HingeLossSchema


class CosineDistanceSchema(BaseLossSchema):
    dim = fields.Int()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return CosineDistanceConfig(**data)

    @post_dump
    def unmake(self, data):
        return CosineDistanceConfig.remove_reduced_attrs(data)


class CosineDistanceConfig(BaseLossConfig):
    """Adds a cosine-distance loss to the training procedure.

    Note that the function assumes that `predictions` and `labels` are already unit-normalized.

    WARNING: `weights` also supports dimensions of 1, but the broadcasting does
    not work as advertised, you'll wind up with weighted sum instead of weighted
    mean for any but the last dimension. This will be cleaned up soon, so please
    do not rely on the current behavior for anything but the shapes documented for
    `weights` below.

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: CosineDistance
      # other model properties
    ```
    """
    IDENTIFIER = 'CosineDistance'
    SCHEMA = CosineDistanceSchema

    def __init__(self,
                 dim,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0,
                 name=None,
                 collect=True):
        self.dim = dim
        super(CosineDistanceConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)


class PoissonLossSchema(BaseLossSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PoissonLossConfig(**data)

    @post_dump
    def unmake(self, data):
        return PoissonLossConfig.remove_reduced_attrs(data)


class PoissonLossConfig(BaseLossConfig):
    """Adds a poisson loss to the training procedure.

    Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: PoissonLoss
      # other model properties
    ```
    """
    IDENTIFIER = 'PoissonLoss'
    SCHEMA = PoissonLossSchema


class KullbackLeiberDivergenceSchema(BaseLossSchema):
    dim = fields.Int()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return KullbackLeiberDivergenceConfig(**data)

    @post_dump
    def unmake(self, data):
        return KullbackLeiberDivergenceConfig.remove_reduced_attrs(data)


class KullbackLeiberDivergenceConfig(BaseLossConfig):
    """Adds a Kullback leiber diverenge loss to the training procedure.

     Args:
        input_layer: The input true values layer, defaults to labels.
        output_layer: The output layer generated by the network,
            default to last layer of the network.
            If the network has multiple output, you should specify which layer to use.
        weights: Optional `Tensor` whose rank is either 0, or the same rank as
            `labels`, and must be broadcastable to `labels` (i.e., all dimensions must
            be either `1`, or the same as the corresponding `losses` dimension).
        name: operation name.
        collect: add to losses collection.

    Returns:
        A scalar `Tensor` representing the loss value.

    Raises:
        ValueError: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      loss: KullbackLeiberDivergence
      # other model properties
    ```
    """
    IDENTIFIER = 'KullbackLeiberDivergence'
    SCHEMA = KullbackLeiberDivergenceSchema

    def __init__(self,
                 dim,
                 input_layer=None,
                 output_layer=None,
                 weights=1.0, name='KullbackLeiberDivergence',
                 collect=True):
        self.dim = dim
        super(KullbackLeiberDivergenceConfig, self).__init__(
            input_layer, output_layer, weights, name, collect)


class LossSchema(BaseMultiSchema):
    __multi_schema_name__ = 'loss'
    __configs__ = {
        AbsoluteDifferenceConfig.IDENTIFIER: AbsoluteDifferenceConfig,
        MeanSquaredErrorConfig.IDENTIFIER: MeanSquaredErrorConfig,
        LogLossConfig.IDENTIFIER: LogLossConfig,
        HuberLossConfig.IDENTIFIER: HuberLossConfig,
        ClippedDeltaLossConfig.IDENTIFIER: ClippedDeltaLossConfig,
        SoftmaxCrossEntropyConfig.IDENTIFIER: SoftmaxCrossEntropyConfig,
        SigmoidCrossEntropyConfig.IDENTIFIER: SigmoidCrossEntropyConfig,
        HingeLossConfig.IDENTIFIER: HingeLossConfig,
        CosineDistanceConfig.IDENTIFIER: CosineDistanceConfig,
        KullbackLeiberDivergenceConfig.IDENTIFIER: KullbackLeiberDivergenceConfig,
    }